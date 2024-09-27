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
from .models import Product, SearchedProduct
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
from .forms import SignUpForm



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



def home(request):
    new_arrivals = Product.objects.filter(section='new_arrival')[:10]
    most_popular = Product.objects.filter(section='most_popular')[:10]
    categories = Category.objects.all()
        
    item_count = get_cart_item_count(request)

            
    faqs = FAQ.objects.filter(is_visible=True)
    initial_faqs = faqs[:2]
    extra_faqs = faqs[2:]

    return render(request, 'home.html', {
        'quantity': item_count,
        'categories': categories,
        'new_arrivals': new_arrivals,
        'most_popular': most_popular,


        'initial_faqs': initial_faqs,
        'extra_faqs': extra_faqs,
    })



def category(request):
    return render(request, 'category.html', {})


def policy(request):
    return render(request, 'policies.html')



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    more_products = Product.objects.all().exclude(id=product.id)[:5]
    categories = Category.objects.all()
    product_categories = product.category.all()
    #related_products = Product.objects.filter(category__in=product_categories).exclude(id=product.id)[:5]
    related_products = Product.objects.filter(category__in=product_categories).exclude(id=product.id).distinct()[:5]


    item_count = get_cart_item_count(request)
            
    context = {
        'quantity': item_count,
        'categories': categories,
        'product': product,
        'related_products': related_products,
        'more_products': more_products,
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

    profile_data = {}
    if request.user.is_authenticated:
        user_profile, created = Profile.objects.get_or_create(user=request.user)
        profile_data = {
            'delivery_location': user_profile.delivery_location or '',
            'name': request.user.get_full_name() or request.user.username,
            'phone_number': user_profile.phone_number or '',
        }

    context = {
        'categories': categories,
        'quantity': item_count,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'discount': discount,
        'total': total,
        'order_note': request.session.get('order_note', ''),
        'profile_data': profile_data,
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
        all_products = Product.objects.filter(category=category)
    else:
        all_products = Product.objects.all()
    
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

#@login_required
#@require_POST
def initialize_payment(request):
    if request.method == 'POST':

        delivery_location = request.POST.get('delivery_location', '').strip()
        name = request.POST.get('name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()

        # Ensure all required fields are provided
        if not all([delivery_location, name, phone_number]):
            messages.error(request, "Please fill out all required fields.")
            return redirect('cart') 
        
        # Validate name
        if not re.match(r'^[a-zA-Z\s]+$', name):
            messages.error(request, "Name should only contain letters and spaces.")
            return redirect('cart')

        # Validate phone number
        if not re.match(r'^\d{10,14}$', phone_number):
            messages.error(request, "Please enter a valid phone number (10-14 digits).")
            return redirect('cart')

        #cart = get_object_or_404(Cart, user=request.user)
        
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
        else:
            cart = get_or_create_guest_cart(request)

        total_amount = calculate_total(cart)
        amount_in_kobo = int(total_amount * 100)

        order_note = request.POST.get('order_note')

        # Generate a random payment reference
        payment_reference = f"ORDER-{uuid.uuid4().hex[:8].upper()}"

        order = Order.objects.create(
            
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key if not request.user.is_authenticated else None,
            delivery_location=delivery_location,
            name=name,
            phone_number=phone_number,
            order_note=order_note,
            total_amount=total_amount,
            payment_reference=payment_reference,
            status='pending'
        )

        # Create OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "amount": amount_in_kobo,
            "email": request.user.email if request.user.is_authenticated else "guest@example.com",
            "callback_url": request.build_absolute_uri(reverse('payment_callback')),
            "reference": order.payment_reference,
        }

        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers=headers,
            json=data
        )
        response_data = response.json()
        if response.status_code == 200:
            # After creating the order
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "orders",
                {
                    "type": "new_order",
                    "order_id": order.id
                }
            )

            return redirect(response_data['data']['authorization_url'])
        else:
            error_message = response_data.get('message', 'Unknown error occurred')
            order.delete()  # Delete the order if payment initialization fails
            return JsonResponse({
                'error': 'Payment initialization failed',
                'message': error_message,
                'details': response_data
            }, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def payment_callback(request):
    reference = request.GET.get('reference')
    if verify_payment(reference):
        order = get_object_or_404(Order, payment_reference=reference)
        
        order.paid = True
        order.status = 'processing'
        order.save()

        #Cart.objects.filter(user=request.user).delete()

        
        if request.user.is_authenticated:
            Cart.objects.filter(user=request.user).delete()
        else:
            if 'cart_id' in request.session:
                Cart.objects.filter(id=request.session['cart_id']).delete()
                del request.session['cart_id']


        return redirect('home')
    else:
        return redirect('cart')


def verify_payment(reference):
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers=headers
    )
    if response.status_code == 200:
        response_data = response.json()
        return response_data['data']['status'] == 'success'
    return False


def calculate_total(cart):

    subtotal = Decimal('0.00')
    for item in cart.items.all():
        product = Product.objects.get(id=item.product.id)
        quantity = item.quantity
        total_price = product.price * quantity
        subtotal += total_price

    settings = PaymentSettings.objects.first()  
    if not settings:
        settings = PaymentSettings.objects.create()

    tax = subtotal * settings.tax_rate
    shipping = settings.shipping_rate
    discount = settings.discount_rate

    return subtotal + tax + shipping - discount




# User Auth

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.email = form.cleaned_data.get('email')
            user.profile.phone_number = form.cleaned_data.get('phone_number')
            user.profile.delivery_location = form.cleaned_data.get('delivery_location')

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
    return render(request, 'signup.html', {'form': form})


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