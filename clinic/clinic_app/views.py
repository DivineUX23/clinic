from .models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Cart, CartItem, Category, Order, OrderItem, PaymentSettings
from django.db.models import F
from django.utils.crypto import get_random_string
from django.views.decorators.http import require_POST
from decimal import Decimal
import datetime
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
from django.contrib import messages


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

def home(request):
    new_arrivals = Product.objects.filter(section='new_arrival')
    most_popular = Product.objects.filter(section='most_popular')
    categories = Category.objects.all()
    

    cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
    if cart:  
        item_count = cart.items.count()
    else:
        item_count = 0
        
    faqs = FAQ.objects.filter(is_visible=True)
    initial_faqs = faqs[:2]  # Show first 2 FAQs initially
    extra_faqs = faqs[2:]    # Remaining FAQs

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


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]
    more_products = Product.objects.all().exclude(id=product.id)[:5]
    
    categories = Category.objects.all()
    
    cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
    if cart:  
        item_count = cart.items.count()
    else:
        item_count = 0
        
    context = {
        'quantity': item_count,
        'categories': categories,
        'product': product,
        'related_products': related_products,
        'more_products': more_products,
    }
    return render(request, 'product.html', context)



def add_to_cart(request):
    print("add_to_cart view called")
    if request.method == 'POST':
        print("POST request received")
        
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        print(f"Product ID: {product_id}, Quantity: {quantity}")

        product = get_object_or_404(Product, id=product_id)
        #cart = get_cart(request)
            
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
        print(f"Cart retrieved/created. Cart ID: {cart.id}, Created: {created}")
            
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity = F('quantity') + quantity
        cart_item.save()
        print(f"Cart item saved. Created: {created}, Quantity: {cart_item.quantity}")
        return JsonResponse({'success': True, 'cart_quantity': cart.items.count()})
    print("Non-POST request received")
    return JsonResponse({'success': False}, status=400)






def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def cart_view(request):

    cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
    cart_items = []
    subtotal = Decimal('0.00')
    
    if cart:    
        for item in cart.items.all():
            product = Product.objects.get(id=item.product.id)
            quantity = item.quantity
            total_price = product.price * quantity
            subtotal += total_price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price,
            })
        item_count = cart.items.count()
    else:
        item_count = 0
    
    settings = PaymentSettings.objects.first()  
    if not settings:
        settings = PaymentSettings.objects.create()

    tax = subtotal * settings.tax_rate
    shipping = settings.shipping_rate
    discount = settings.discount_rate

    total = subtotal + tax + shipping - discount

    categories = Category.objects.all()

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
    }
    print(context)  # This will print the context in the console for debugging.

    return render(request, 'cart.html', context)

@require_POST
def update_cart(request):
    cart = get_cart(request)
    product_id = request.POST.get('product_id')
    action = request.POST.get('action')
    
    if product_id in cart:
        if action == 'increase':
            cart[product_id]['quantity'] += 1
        elif action == 'decrease':
            cart[product_id]['quantity'] -= 1
            if cart[product_id]['quantity'] <= 0:
                del cart[product_id]
    
    save_cart(request, cart)
    return redirect('cart')

@require_POST
def update_order_note(request):
    order_note = request.POST.get('order_note', '')
    request.session['order_note'] = order_note
    return redirect('cart')



@require_POST
def remove_from_cart(request):
    
    cart = Cart.objects.filter(session_key=request.session.session_key).first()        
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
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

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

    paginator = Paginator(products, 20)  # Show 20 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)

    cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
    if cart:  
        item_count = cart.items.count()
    else:
        item_count = 0
        
    context = {
        'quantity': item_count,
        'products': products,
        'sort': sort,
        'categories': categories,
        'total': len(products)
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

        cart = get_object_or_404(Cart, session_key=request.session.session_key)
        total_amount = calculate_total(cart)
        amount_in_kobo = int(total_amount * 100)

        order_note = request.POST.get('order_note')

        # Create the order (unpaid at this point)
        order = Order.objects.create(
            session_key=request.session.session_key,
            delivery_location=delivery_location,
            name=name,
            phone_number=phone_number,
            order_note=order_note,
            total_amount=total_amount,
            payment_reference=f"cart_{request.session.session_key}_{total_amount}",
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

        Cart.objects.filter(session_key=order.session_key).delete()

        return redirect('home')
    else:
        return redirect('cart')


def verify_payment(reference):
    # Verify the payment with Paystack
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
        
        # Only allow updating the status field
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
