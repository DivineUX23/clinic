from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Category, Order, PaymentSettings, SearchedProduct, ShippingInfo
from django.db.models import F
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
from django.urls import reverse
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decimal import Decimal
from django.contrib import messages
from .models import Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignUpForm, OrderForm

import json
import logging



#API IMPORTS
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import OrderSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import FAQ
from .helpers import (get_or_create_guest_cart, get_cart_item_count, 
                     create_authenticated_order, create_session_order, update_authenticated_order,
                     update_session_order, verify_payment, calculate_total, get_shipping_rates, 
                     create_shipment, get_categories, make_paystack_request, handle_payment_error,
                    clear_cart, get_or_create_cart, send_admin_notification, send_user_notification)


logger = logging.getLogger(__name__)

create_authenticated_order


def home(request):
    categories = Category.objects.all()
    item_count = get_cart_item_count(request)
    
    faqs = FAQ.objects.filter(is_visible=True)
    initial_faqs = faqs[:2]
    extra_faqs = faqs[2:]

    return render(request, 'home.html', {
        'quantity': item_count,
        'categories': categories,
        'initial_faqs': initial_faqs,
        'extra_faqs': extra_faqs,
    })

def product_api(request, section):
    page_number = request.GET.get('page', 1)
    items_per_page = 20  # Adjust this number as needed

    if section == 'new-arrivals':
        products = Product.objects.filter(section='new_arrival', available=True)[:50]

    elif section == 'most-popular':
        products = Product.objects.filter(section='most_popular', available=True)[:50]
    else:
        return JsonResponse({'error': 'Invalid section'}, status=400)

    paginator = Paginator(products, items_per_page)
    page_obj = paginator.get_page(page_number)

    product_data = [
        {
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'image_url': product.image.url if product.image else None,
            'slug': product.slug,
            'stock': product.stock,
            'available': product.available,
        }
        for product in page_obj
    ]

    pagination_data = {
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    }

    return JsonResponse({
        'products': product_data,
        'pagination': pagination_data,
    })


def user_orders(request):
    # Get filter and sort parameters
    status_filter = request.GET.get('status', 'all')
    sort_by = request.GET.get('sort', '-created_at')

    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = Order.objects.filter(session_key=request.session.session_key)

    if status_filter != 'all':
        orders = orders.filter(shipment_status=status_filter)

    orders = orders.order_by(sort_by)

    categories = Category.objects.all()

    # Pagination
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'sort_by': sort_by,
        'categories': categories,

    }
    return render(request, 'user_orders.html', context)









def category(request):
    return render(request, 'category.html', {})


def policy(request):
    return render(request, 'policies.html')



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    #product.increment_view_count()
    #more_products = Product.objects.all().exclude(id=product.id)[:5]
    more_products = Product.objects.filter(available=True).exclude(id=product.id)[:5]
    categories = Category.objects.all()
    product_categories = product.category.all()
    #related_products = Product.objects.filter(category__in=product_categories).exclude(id=product.id)[:5]
    related_products = Product.objects.filter(category__in=product_categories, available=True).exclude(id=product.id).distinct()[:5]

    all_products = Product.objects.filter(available=True)

    item_count = get_cart_item_count(request)
            
    context = {
        'quantity': item_count,
        'categories': categories,
        'product': product,
        'related_products': related_products,
        'more_products': more_products,
        'total_product_count': all_products.count()
    }
    return render(request, 'product.html', context)




def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        product.increment_add_count()            
        cart = get_or_create_cart(request)
        
        if cart:
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            if not created:
                cart_item.quantity = F('quantity') + quantity
            cart_item.save()

            return JsonResponse({'success': True, 'cart_quantity': cart.items.count()})

    return JsonResponse({'success': False}, status=400)






def cart_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = get_or_create_guest_cart(request)
    
    cart_items = []
    subtotal = Decimal('0.00')
    item_count = 0
    
    if cart:
        for item in cart.items.select_related('product').all():
            product = item.product
            quantity = item.quantity
            total_price = product.price * quantity
            subtotal += total_price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price,
            })
        item_count = len(cart_items)
    
    settings = PaymentSettings.objects.first()  
    if not settings:
        settings = PaymentSettings.objects.create()

    tax = subtotal * settings.tax_rate
    shipping = settings.shipping_rate
    discount = settings.discount_rate

    total = subtotal + tax + shipping - discount


    categories = Category.objects.all()

    initial_data = {}
    if request.user.is_authenticated:
        user_profile, _ = Profile.objects.get_or_create(user=request.user)
        if user_profile.delivery_location:
            initial_data = {                
                'address': user_profile.delivery_location.formatted_address,
                'email': request.user.email,
                'first_name': request.user.first_name if request.user.first_name else request.user.get_full_name(),
                'last_name':  request.user.last_name if request.user.last_name else None,
                'phone_number': user_profile.phone_number,
            }

    form = OrderForm(initial=initial_data)


    #get shipbubble categor
    order_category_raw = get_categories()
    order_category = [{'id': item['category_id'], 'name': item['category']} for item in order_category_raw]

    print(order_category)
    # Prepare data for dynamic dropdowns
    #countries = list(Country.objects.values('id', 'name'))
    #states = list(Region.objects.values('id', 'name', 'country_id'))
    #cities = list(City.objects.values('id', 'name', 'region_id'))


    # Get the 5 most recent processing or failed orders
    try:
        if request.user.is_authenticated:
    
            recent_orders = Order.objects.filter(
                user=request.user,
                status__in=['processing', 'failed']
            ).order_by('-created_at')[:5]

        else:
            order_id = request.session.get('order_id')
            recent_orders = Order.objects.filter(
                id=order_id, 
                user__isnull=True,
                status__in=['processing', 'failed']
                ).order_by('-created_at')[:5]

    except Exception as e:
        print(f"Error fetching recent orders: {e}")
        messages.error(request, f"Error fetching recent orders: {e}")


    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'discount': discount,
        'total': total,
        'form': form,
        #'countries': countries,
        #'states': states,
        #'cities': cities,

        'recent_orders': recent_orders,
        'order_category': order_category,
        'categories': categories,
        'quantity': item_count,
    }
    return render(request, 'cart.html', context)




@require_POST
def update_cart(request):
    cart = get_or_create_cart(request)
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')

    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if action == 'increase':
        cart_item.quantity = F('quantity') + 1
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity = F('quantity') - 1
        else:
            cart_item.delete()
            #return redirect('cart')
    
    cart_item.save()
    return redirect('cart')




@require_POST
def update_order_note(request):
    cart = get_or_create_cart(request)
    order_note = request.POST.get('order_note', '')
    cart.order_note = order_note
    cart.save()
    return redirect('cart')




@require_POST
def remove_from_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = get_or_create_guest_cart(request)
    
    if not cart:
        messages.error(request, "Cart not found.")

    product_id = request.POST.get('product_id')
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
    if cart_item:
        cart_item.delete()

    if not cart.items.exists():
        cart.delete()
    cart.save()
    
    return redirect('cart')



def product_list(request, category_id=None):

    if category_id:
        category = Category.objects.get(id=category_id)
        all_products = Product.objects.filter(category=category, available=True)
    else:
        all_products = Product.objects.filter(available=True)
    
    products = all_products

    categories = Category.objects.all()
    
    sort = request.GET.get('sort', 'latest')

    if sort == 'low-high':
        products = products.order_by('price')
    elif sort == 'high-low':
        products = products.order_by('-price')
    elif sort == 'a-z':
        products = products.order_by('name')
    elif sort == 'z-a':
        products = products.order_by('-name')
    else:  # latest
        products = products.order_by('-created_at')

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    item_count = get_cart_item_count(request)

    context = {
        'quantity': item_count,
        'products': products,
        'page_obj': products,
        'is_paginated': products.has_other_pages(),
        'sort': sort,
        'categories': categories,
        'total': all_products.count()
    }
    return render(request, 'products.html', context)



def search_products(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )[:10]  # Limit to 10 results
        
        if products.exists():
            results = [{'id': p.id, 'name': p.name, 'category': p.category.name, 'url': p.get_absolute_url()} for p in products]
            return JsonResponse({'exists': True, 'results': results})
        else:
            # Save the searched product that doesn't exist
            SearchedProduct.objects.create(name=query)
            return JsonResponse({'exists': False, 'message': 'Product not found'})
    return JsonResponse({'exists': False, 'message': 'No query provided'})



#PAYMENT:

from datetime import datetime
# User Auth
from .models import Location
import json


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        """
        # Get the selected country and state from the POST data create_order
        country_id = request.POST.get('country')
        state_id = request.POST.get('state')
        
        # Populate the state and city querysets based on the selected country and state
        if country_id:
            form.fields['state'].queryset = Region.objects.filter(country_id=country_id)
        if state_id:
            form.fields['city'].queryset = City.objects.filter(region_id=state_id)
        """
        
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone_number = form.cleaned_data.get('phone_number')


            location = Location.formatted_address=form.cleaned_data.get('address')
            location.save()
            
            # Associate the Location with the user's profile
            user.profile.delivery_location = location
            user.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully signed up!")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }

    return render(request, 'signup.html', context)
    #return render(request, 'signup.html', {'form': form})



def signin_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully signed in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})





#update_authenticated_order
def initialize_payment(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        print(form)
        if form.is_valid():
            if request.user.is_authenticated:
                order = create_authenticated_order(request, form)
                cart = get_object_or_404(Cart, user=request.user)
            else:
                order = create_session_order(request, form)
                cart = get_or_create_guest_cart(request)

            total_amount = calculate_total(cart)
            shipping_rates = get_shipping_rates(order, cart.items.all())

            print(f"\n\n shipping_rates user------------------'{shipping_rates}'\n\n")

            if shipping_rates is None:
                messages.error(request, f"Shipbubble Error: Error accessing riders in your location, try again")
                return redirect('cart')


            if 'status' in shipping_rates and shipping_rates.get('status') == 'success':

                if 'data' in shipping_rates:
                    shipping_rates = shipping_rates.get('data', {})
                else:
                    messages.error(request, f"Shipbubble Error: {shipping_rates.get('message')}")
                    return redirect('cart')
            elif 'status' in shipping_rates and shipping_rates.get('status') == 'failed':

                messages.error(request, f"Shipbubble Error: {shipping_rates.get('message')}")
                return redirect('cart')
            else:
                messages.error(request, f"Shipbubble Error: {shipping_rates.get('message')}")
                return redirect('cart')
            
            context = {
                'order': order,
                'shipping_rates': shipping_rates,
            }
            return render(request, 'shipping_options.html', context)

        else:
            
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    return redirect('cart')







# PAYMENT: order.paid

def make_payment(request, order_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            order = get_object_or_404(Order, id=order_id)
        else:
            order = request.session.get('order')
            if not order:
                messages.error(request, "No order found in session.")
                return redirect('cart')

        order = get_object_or_404(Order, id=order_id)
        chosen_rate = request.POST.get('chosen_rate')
        request_token = request.POST.get('request_token')

        if not chosen_rate:
            messages.error(request, "Please choose a shipping method.")
            return redirect('make_payment', order_id=order_id)
        
        try:
            chosen_rate_data = json.loads(chosen_rate)

            #if request.user.is_authenticated:
            shipping_info, created = ShippingInfo.objects.get_or_create(order=order)
            shipping_info.service_code = chosen_rate_data['service_code']
            shipping_info.courier_id = chosen_rate_data['courier_id']
            shipping_info.shipping_cost = Decimal(chosen_rate_data['total'])
            shipping_info.request_token = chosen_rate_data['request_token']
            shipping_info.save()
            """
            else:
                guest_info['shipping_info'] = {
                    'service_code': chosen_rate_data['service_code'],
                    'courier_id': chosen_rate_data['courier_id'],
                    'shipping_cost': str(chosen_rate_data['total'])
                }
                request.session.modified = Truerequest_token
            """
            amount_in_kobo = int((order.total_amount + shipping_info.shipping_cost) * 100)
            guest_info = order.request.session.get('guest_user', {}) if hasattr(order, 'request') else {}

            # Update the paystack_data creation:
            paystack_data = {
                "amount": amount_in_kobo,
                "email": request.user.email if request.user.is_authenticated else guest_info['email'],
                "callback_url": request.build_absolute_uri(reverse('payment_callback')),
                "reference": order.payment_reference if request.user.is_authenticated else guest_info['payment_reference'],
            }
            
            print(paystack_data)
            paystack_response = make_paystack_request("https://api.paystack.co/transaction/initialize", paystack_data)
            
            if paystack_response.get('status'):
                # Notify about new order
                notify_new_order(order.id)
                return redirect(paystack_response['data']['authorization_url'])
            else:
                return handle_payment_error(paystack_response)
        
        except json.JSONDecodeError:
            messages.error(request, "Invalid shipping option data.")
            return redirect('make_payment', order_id=order_id)
        except KeyError:
            messages.error(request, "Incomplete shipping option data.")
            return redirect('make_payment', order_id=order_id)

    return render(request, 'shipping_options.html', {'order_id': order_id})



def payment_callback(request):
    reference = request.GET.get('reference')
    if verify_payment(reference):
        # Replace the existing order retrieval with:
        if request.user.is_authenticated:
            order = get_object_or_404(Order, payment_reference=reference)
        else:
            order = request.session.get('order')
            if not order or order.payment_reference != reference:
                messages.error(request, "Invalid order reference.")
                return redirect('cart')

        # Create shipment
        shipment_created = create_shipment(order)
        clear_cart(request)

        if shipment_created and shipment_created.get('status') == 'success':
            shipment_data = shipment_created['data']
            
            #if request.user.is_authenticated:
                #update_authenticated_order(order, shipment_data)
            #else:
                #update_session_order(request, order, shipment_data)user_orders
            update_authenticated_order(order, shipment_data)

            send_admin_notification(order, shipment_success=True)
            send_user_notification(order, success=True)

            messages.success(request, "Payment successful! Your shipment is on its way.")
            return redirect("user_orders")
            #return redirect(shipment_data['tracking_url'])
            #return redirect('home')
        else:
            order.paid = True
            order.status = 'confirmed'
            order.save()
            send_admin_notification(order, shipment_success=False)
            send_user_notification(order, success=False)

            messages.error(request, "Payment successful, but shipment creation failed. Please contact support.")
    else:
        messages.error(request, "Payment verification failed.")
    
    return redirect('cart')




def notify_new_order(order_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "orders",
        {
            "type": "new_order",
            "order_id": order_id
        }
    )




#WEBHOOK
import hashlib
import hmac
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings

@csrf_exempt
def shipbubble_webhook(request):
    if request.method == 'POST':
        # Verify the webhook signature
        signature = request.headers.get('x-ship-signature')
        if not verify_signature(request.body, signature):
            return HttpResponse(status=403)

        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        # Process the webhook
        order_id = payload.get('order_id')
        status_code = payload.get('status_code')

        if order_id and status_code:
            try:
                shipment = ShippingInfo.objects.get(shipment_id=order_id)
                shipment.shipment_status = status_code
                shipment.order.status = status_code
                shipment.save()
            except Order.DoesNotExist:
                pass

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

def verify_signature(payload, signature):
    secret_key = settings.SHIPBUBBLE_API_KEY 
    computed_signature = hmac.new(secret_key.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(computed_signature, signature)















def toggle_dark_mode(request):
    if 'dark_mode' in request.session:
        request.session['dark_mode'] = not request.session['dark_mode']
    else:
        request.session['dark_mode'] = True
    return redirect(request.META.get('HTTP_REFERER', '/'))









#API CODE

class FlexiblePagination(PageNumberPagination):
    page_size = 20  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

class OrderList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = FlexiblePagination
    
    def get_queryset(self):
        queryset = Order.objects.all()
        status = self.request.query_params.get('status', None)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset


class OrderDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        
        if 'status' in serializer.validated_data:
            instance.status = serializer.validated_data['status']
            instance.save()

            # Notify connected clients about the status change
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "orders",
                {
                    "type": "order_updated",
                    "order_id": instance.id
                }
            )

            return Response(serializer.data)
        else:
            return Response({"detail": "Only status field can be updated."}, status=status.HTTP_400_BAD_REQUEST)






















#--------------------

def test_api(request):
    return render(request, 'app.html')


import requests
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import logging

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
def proxy_view(request, path):
    base_url = 'https://no1logsmarketplace.com/api/v1/'
    url = f'{base_url}{path}'
    
    headers = {
        'Authorization': f'Bearer NO1LOGS_YFxGbP33RHzC21waRJ',
        'Accept': 'application/json'
    }

    try:
        if request.method == 'GET':
            response = requests.get(url, headers=headers)
        elif request.method == 'POST':
            response = requests.post(url, json=request.POST, headers=headers)

        # Log the response for debugging
        logger.info(f"API Response: Status {response.status_code}, Content: {response.text}")

        # Return the raw response
        return HttpResponse(
            content=response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'text/plain')
        )

    except requests.RequestException as e:
        logger.error(f"Request Exception: {str(e)}")
        return HttpResponse(f"API request failed: {str(e)}", status=500)