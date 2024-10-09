from .models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Category, Order, OrderItem, PaymentSettings
from django.db.models import F
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView
from .models import Product, SearchedProduct, SenderAddress
from django.conf import settings
from django.urls import reverse
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decimal import Decimal
import re
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignUpForm, OrderForm

import json
import logging
from datetime import datetime
from django.core.cache import cache



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



logger = logging.getLogger(__name__)


def get_or_create_guest_cart(request):
    cart_id = request.session.get('cart_id')
    if cart_id:
        cart = Cart.objects.filter(id=cart_id, user__isnull=True).first()
        if cart:
            return cart
    
    cart = Cart.objects.create()
    request.session['cart_id'] = cart.id
    return cart

def get_cart_item_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        cart = get_or_create_guest_cart(request)
    return cart.items.count() if cart else 0


from django.utils import timezone
from datetime import timedelta




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
    items_per_page = 10  # Adjust this number as needed

    if section == 'new-arrivals':
        #thirty_days_ago = timezone.now() - timedelta(days=30)
        #products = Product.objects.filter(created_at__gte=thirty_days_ago).order_by('-created_at')
        products = Product.objects.filter(section='new_arrival', available=True)[:50]

    elif section == 'most-popular':
        #products = Product.objects.order_by('-view_count')
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











from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Order
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Order

@login_required
def user_orders(request):
    # Get filter and sort parameters
    status_filter = request.GET.get('status', 'all')
    sort_by = request.GET.get('sort', '-created_at')

    # Base queryset
    orders = Order.objects.filter(user=request.user)

    # Apply status filter
    if status_filter != 'all':
        orders = orders.filter(shipment_status=status_filter)

    # Apply sorting
    orders = orders.order_by(sort_by)

    # Pagination
    paginator = Paginator(orders, 10)  # create_shipment
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
        'sort_by': sort_by,
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



def get_or_create_cart(request):
    if request.user.is_authenticated:
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            return cart
        except Exception as e:
            messages.error(request, f"Error creating cart: {str(e)}")
            return None
    else:
        return get_or_create_guest_cart(request)






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
                'street_no': user_profile.delivery_location.street_no,
                'street': user_profile.delivery_location.street,
                'country': user_profile.delivery_location.country,
                'state': user_profile.delivery_location.state,
                'city': user_profile.delivery_location.city,
                'postal_code': user_profile.delivery_location.postal_code,                                
                'first_name': user_profile.first_name if user_profile.first_name else request.user.username or request.user.get_full_name(),
                'last_name':  user_profile.last_name if user_profile.last_name else None,
                'phone_number': user_profile.phone_number,
            }

    form = OrderForm(initial=initial_data)


    #get shipbubble categor
    order_category_raw = get_categories()
    order_category = [{'id': item['category_id'], 'name': item['category']} for item in order_category_raw]

    print(order_category)
    # Prepare data for dynamic dropdowns
    countries = list(Country.objects.values('id', 'name'))
    states = list(Region.objects.values('id', 'name', 'country_id'))
    cities = list(City.objects.values('id', 'name', 'region_id'))


    # Get the 5 most recent processing or failed orders
    recent_orders = Order.objects.filter(
        user=request.user,
        status__in=['processing', 'failed']
    ).order_by('-created_at')[:5]

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'discount': discount,
        'total': total,
        'form': form,
        'countries': countries,
        'states': states,
        'cities': cities,

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
"""
Before initialize payment, choose category id, a pop shows all all the available curiors and ask them to choose 
and confirm then payment countinues to paystack initialize payments. 

clcik buy button takes here:::::

"""
from datetime import datetime
# User Auth
from .models import Location
from cities_light.models import Country, Region, City
import json


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        
        # Get the selected country and state from the POST data
        country_id = request.POST.get('country')
        state_id = request.POST.get('state')
        
        # Populate the state and city querysets based on the selected country and state
        if country_id:
            form.fields['state'].queryset = Region.objects.filter(country_id=country_id)
        if state_id:
            form.fields['city'].queryset = City.objects.filter(region_id=state_id)
        
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')


            # Create and save the Location object
            location = Location(                
                street_no=form.cleaned_data.get('street_no'),
                street=form.cleaned_data.get('street'),
                country=form.cleaned_data.get('country'),
                state=form.cleaned_data.get('state'),
                city=form.cleaned_data.get('city'),
                postal_code=form.cleaned_data.get('postal_code')
            )
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


    # Prepare data for dynamic dropdowns
    countries = list(Country.objects.values('id', 'name'))
    states = list(Region.objects.values('id', 'name', 'country_id'))
    cities = list(City.objects.values('id', 'name', 'region_id'))

    context = {
        'form': form,
        'countries_json': json.dumps(countries),
        'states_json': json.dumps(states),
        'cities_json': json.dumps(cities),
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















def initialize_payment(request):
    if request.method == 'POST':

        form = OrderForm(request.POST)

        # Print raw POST data
        print("Raw POST data:")
        print(json.dumps(request.POST, indent=2))

        form = OrderForm(request.POST)
        print("Form instance:")
        if form.is_valid():
            # Process the form data
            street_no = form.cleaned_data['street_no']
            street = form.cleaned_data['street']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            city = form.cleaned_data['city']
            postal_code = form.cleaned_data['postal_code']
            name = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data.get('email', '')
            order_note = form.cleaned_data.get('order_note', '')

            order_category = form.cleaned_data.get('order_category')

            # Handle location for authenticated users Order.cate
            if request.user.is_authenticated:
                profile = request.user.profile
                location = handle_authenticated_user_location(profile, form.cleaned_data)
                cart = get_object_or_404(Cart, user=request.user)
            else:
                # For non-authenticated users, always create a new location
                location = Location.objects.create(
                    street_no=street_no,
                    street=street,
                    country=country,
                    state=state,
                    city=city,
                    postal_code=postal_code
                )
                cart = get_or_create_guest_cart(request)

            total_amount = calculate_total(cart)
            payment_reference = f"ORDER-{uuid.uuid4().hex[:8].upper()}"
            order = create_order(request, location, form.cleaned_data, total_amount, payment_reference)
            shipping_rates = get_shipping_rates(order, cart.items.all())

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



# PAYMENT:

def make_payment(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        chosen_rate = request.POST.get('chosen_rate')
        request_token = request.POST.get('request_token')

        if not chosen_rate:
            messages.error(request, "Please choose a shipping method.")
            return redirect('make_payment', order_id=order_id)
        
        try:
            chosen_rate_data = json.loads(chosen_rate)
            
            order.service_code = chosen_rate_data['service_code']
            order.courier_id = chosen_rate_data['courier_id']
            order.shipping_cost = Decimal(chosen_rate_data['total'])
            order.request_token = request_token
            order.save()
            
            amount_in_kobo = int((order.total_amount + order.shipping_cost) * 100)
            

            paystack_data = {
                "amount": amount_in_kobo,
                "email": request.user.email if request.user.is_authenticated else order.email,
                "callback_url": request.build_absolute_uri(reverse('payment_callback')),
                "reference": order.payment_reference,
            }
            
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
        order = get_object_or_404(Order, payment_reference=reference)
        
        # Create shipment
        shipment_created = create_shipment(order)
        print(shipment_created)


        if shipment_created['status'] == 'success':
            shipment_data = shipment_created['data']
                        
            order.shipment_order_id = shipment_data['order_id']
            order.courier_name = shipment_data['courier']['name']
            order.courier_email = shipment_data['courier']['email']
            order.courier_phone = shipment_data['courier']['phone']
            order.shipment_status = shipment_data['status']
            order.shipping_fee = shipment_data['payment']['shipping_fee']
            order.package_weight = shipment_data['package_weight']
            order.tracking_url = shipment_data['tracking_url']
            order.shipment_date = timezone.now()
            order.paid = True
            order.status = 'processing'
            order.save()

            # Clear the cart Shipping method
            clear_cart(request)

            success_message = (
                f"Payment successful! Your shipment is on its way.\n"
                f"Tracking Code: {order.tracking_number}\n"
                f"Courier: {order.courier_name}\n"
                f"Status: {order.status}\n"
                f"Tracking URL: {order.tracking_url}"
            )
            
            #messages.success(request, success_message)
            messages.success(request, "Payment successful! Your shipment is on its way")
            print("SUCESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            return redirect('home')
        
        else:
            messages.error(request, "Payment successful, but shipment creation failed. Please contact support.")
            return redirect('cart')
    else:
        messages.error(request, "Payment verification failed.")
        return redirect('cart')


def verify_payment(reference):
    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = make_paystack_request(verify_url, method='GET')
    return response.get('status') and response['data']['status'] == 'success'



def calculate_total(cart):
    subtotal = sum(item.product.price * item.quantity for item in cart.items.all())
    settings = PaymentSettings.objects.first() or PaymentSettings.objects.create()
    tax = subtotal * settings.tax_rate
    shipping = settings.shipping_rate
    discount = settings.discount_rate
    return subtotal + tax + shipping - discount



def get_shipping_rates(order, cart_items):
    url = "https://api.shipbubble.com/v1/shipping/fetch_rates"
    
    package_items = [
        {
            "name": item.product.name,
            "description": item.product.description[:100] if item.product.description else "Health related product from JollyLifeHealth",
            "unit_weight": 1,
            "unit_amount": float(item.product.price),
            "quantity": item.quantity
        }
        for item in cart_items
    ]

    data = {
        "sender_address_code": get_sender_address_code(),
        "reciever_address_code": create_or_get_address_code(order), # CHANGE: Fixed typo in 'receiver'
        "pickup_date": datetime.now().strftime("%Y-%m-%d"),
        "category_id": order.order_category if order.order_category else 99652979,
        "package_items": package_items,
        "package_dimension": {
            "length": 10,
            "width": 10,
            "height": 10
        },
        "delivery_instructions": order.order_note if order.order_note else "Handle with care"
    }

    response = make_shipbubble_request(url, data)
    return response.get('data', {})



def create_shipment(order):


    url = "https://api.shipbubble.com/v1/shipping/labels"
    
    data = {
        "request_token": order.request_token,
        "service_code": order.service_code,
        "courier_id": order.courier_id
        }

    print(f"--------------------{data}")
    response = make_shipbubble_request(url, data)
    if response.get('status') == 'success':

        order.tracking_number = response['data']['tracking_url']
        order.save()
        return response
    else:
        logger.error(f"Shipment creation failed for order {order.id}: {response.get('message')}")
        return response




def get_sender_address_code():
    sender_code = cache.get('sender_address_code')
    if sender_code:
        return sender_code

    sender_address = SenderAddress.objects.first()
    if not sender_address:
        logger.error("No sender address found in the database")
        return None

    url = "https://api.shipbubble.com/v1/shipping/address/validate"
    
    
    data = {
        "phone": sender_address.phone_number,
        "email": sender_address.email,
        "name": sender_address.admin.first_name  + " " + "David",
        "address": sender_address.formatted_address
    }
    
    print(data)

    response = make_shipbubble_request(url, data)

    if response.get('status') == 'success':
        sender_code = response['data']['address_code']
        print(f"\n\n response------------------{sender_code}\n\n")

        cache.set('sender_address_code', sender_code, 60*60*24)
        print(f"\n\n chaced response------------------{sender_code}\n\n")

        return sender_code
    else:
        logger.error(f"Error creating sender address: {response.get('message')}")
        print(f"Error creating sender address: {response.get('message')}")

        return None



def create_or_get_address_code(order):
    cache_key = f"address_code_{order.id}"
    address_code = cache.get(cache_key)
    if address_code:
        print(f"\n\n chaced user------------------{address_code}\n\n")
        return address_code

    url = "https://api.shipbubble.com/v1/shipping/address/validate"

    delivery_address = order.delivery_location
    
    #data = {"phone": "07067239473", "email": "Sam@gmail.com", "name": "Mather Osas", "address": "1, Ugbowo, Benin City, Edo State, 4444, Nigeria"}
    
    data = {
        "phone": str(order.phone_number),
        "email": str(order.email),
        "name": f"{str(order.first_name)} {str(order.last_name)}",
        "address": str(delivery_address.formatted_address)
    }
    print(data)

    response = make_shipbubble_request(url, data)
    if response.get('status') == 'success':
        address_code = response['data']['address_code']
        cache.set(cache_key, address_code, 60*60)
        return address_code
    else:
        logger.error(f"Error creating address for order {order.id}: {response.get('message')}")
        return None


def get_categories():
    url = "https://api.shipbubble.com/v1/shipping/labels/categories"
    response = make_shipbubble_request(url, method='GET')  


    print(f"\n\n response------------------{response}\n\n")

    return response.get('data', [])



# Helper functions

def handle_authenticated_user_location(profile, form_data):
    if profile.delivery_location:
        location = profile.delivery_location
        if location_needs_update(location, form_data):
            update_location(location, form_data)
    else:
        location = create_location(form_data)
        profile.delivery_location = location

    update_profile(profile, form_data)
    return location

def location_needs_update(location, form_data):
    return any([
        location.street_no != form_data['street_no'],
        location.street != form_data['street'],
        location.country != form_data['country'],
        location.state != form_data['state'],
        location.city != form_data['city'],
        location.postal_code != form_data['postal_code']
    ])

def update_location(location, form_data):
    for field in ['street_no', 'street', 'country', 'state', 'city', 'postal_code']:
        setattr(location, field, form_data[field])
    location.save()

def create_location(form_data):
    return Location.objects.create(
        street_no=form_data['street_no'],
        street=form_data['street'],
        country=form_data['country'],
        state=form_data['state'],
        city=form_data['city'],
        postal_code=form_data['postal_code']
    )

def update_profile(profile, form_data):
    if profile.phone_number != form_data['phone_number']:
        profile.phone_number = form_data['phone_number']
    if profile.email != form_data['email']:
        profile.email = form_data['email']
    profile.save()


def create_order(request, location, form_data, total_amount, payment_reference):
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=request.session.session_key if not request.user.is_authenticated else None,
        delivery_location=location,
        first_name=form_data['first_name'],
        last_name=form_data['last_name'],
        phone_number=form_data['phone_number'],
        email=form_data['email'],
        order_note=form_data['order_note'],
        total_amount=total_amount,
        payment_reference=payment_reference,
        status='pending',
        order_category=form_data['order_category']
    )

    cart = Cart.objects.get(user=request.user) if request.user.is_authenticated else get_or_create_guest_cart(request)
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity
        )

    return order

def make_shipbubble_request(url, data=None, method='POST'):
    headers = {
        "Authorization": f"Bearer {settings.SHIPBUBBLE_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        else:
            print(f"\n\n data--------------------------00000000000000000000000-{data}\n\n ")

            response = requests.post(url, headers=headers, json=data)
        print(f"\n\n RESPONSE++++++++++++++++++++------------------{response.text}\n\n")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Shipbubble API error: {str(e)}")
        messages.error(f"Shipbubble API error: {str(e)}, Please retry")
        return {'status': 'error', 'message': str(e)}


{"status":"success",
 "message":"Your shipment is on its way Richard Express, you will be notified shortly",
 "data":{"order_id":"SB-E4AA53510EFC","courier":
         {"name":"Richard Express","email":"test2@getdelivry.com","phone":"+2340000000000"},
         "status":"pending",
         "ship_from":
         {"name":"Mather Osas","phone":"+2347067239473",
          "email":"Sam@gmail.com","address":"1, Ugbowo, Benin City, Edo State, 4444, Nigeria",
          "latitude":6.3887708,"longitude":5.6094461},
          "ship_to":{"name":"Mather Osas","phone":"+2347067239473","email":"Sam@gmail.com","address":"1, Ugbowo, Benin City, Edo State, 4444, Nigeria","latitude":6.3887708,"longitude":5.6094461},
          "payment":{"shipping_fee":1450.25,"type":"wallet","status":"completed","currency":"NGN"},
          "items":[{"name":"Data","description":"Handle with care","weight":1,"amount":3000,"quantity":1,"total":3000},
                   {"name":"Chorf","description":"Handle with care","weight":1,"amount":1000,"quantity":1,"total":1000}],
                   "package_weight":2,"tracking_url":"https://trackshipment.shipbubble.com/shipment/SB-E4AA53510EFC","date":"2024-10-08 14:09:17"}}

def make_paystack_request(url, data=None, method='POST'):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        else:
            response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Paystack API error: {str(e)}")
        return {'status': False, 'message': str(e)}



def notify_new_order(order_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "orders",
        {
            "type": "new_order",
            "order_id": order_id
        }
    )



def handle_payment_error(response):
    error_message = response.get('message', 'Unknown error occurred')
    logger.error(f"Payment initialization failed: {error_message}")
    return JsonResponse({
        'error': 'Payment initialization failed',
        'message': error_message,
        'details': response
    }, status=400)




def clear_cart(request):
    if request.user.is_authenticated:
        Cart.objects.filter(user=request.user).delete()
    else:
        if 'cart_id' in request.session:
            Cart.objects.filter(id=request.session['cart_id']).delete()
            del request.session['cart_id']





















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