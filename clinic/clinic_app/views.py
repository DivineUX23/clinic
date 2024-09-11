from django.shortcuts import render
from .models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, CartItem



from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, Cart, CartItem
from django.db.models import F
from django.utils.crypto import get_random_string




from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Product
from decimal import Decimal
import datetime


# Create your views here.
def home(request):
    new_arrivals = Product.objects.filter(section='new_arrival')
    most_popular = Product.objects.filter(section='most_popular')
    categories = Category.objects.all()


    cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
    if cart:  
        item_count = cart.items.count()
    else:
        item_count = 0
        
    return render(request, 'home.html', {
        'quantity': item_count,
        'categories': categories,
        'new_arrivals': new_arrivals,
        'most_popular': most_popular
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
"""
def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    print(f"Cart retrieved/created. Cart ID: {cart.id}, Created: {created}")
    return cart
"""

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







#---------------------


def get_cart(request):
    return request.session.get('cart', {})

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True

def cart_view(request):
    #cart = get_cart(request)
    print(request.session.session_key)
    print("-----------------------", request.session.get('cart'))  # Check if the cart exists in the session.
    #cart = get_object_or_404(Cart, session_key=request.session.session_key)
    #print(cart)

    cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
    cart_items = []
    subtotal = Decimal('0.00')
    
    if cart:    
        for item in cart.items.all():
            print("-----", item.product.id)
            product = Product.objects.get(id=item.product.id)
            print("-----", product)
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
        
    tax = subtotal * Decimal('0.05')  # Assuming 5% tax
    shipping = Decimal('1000.00')  # Flat shipping rate
    discount = Decimal('0.00')  # You can implement discounts later
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
    print(request.session.session_key)
    print("-----------------------", request.session.get('cart'))  # Check if the cart exists in the session.
    #cart = get_object_or_404(Cart, session_key=request.session.session_key)
    #print(cart)

    cart = Cart.objects.filter(session_key=request.session.session_key).first()
        
    product_id = request.POST.get('product_id')

    # Find and remove the item from the cart
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
    if cart_item:
        cart_item.delete()  # Remove the item from the database
    
    # Check if cart is empty and remove it if needed
    if not cart.items.exists():
        cart.delete()


    # Save the cart if modifications were made to the cart itself
    cart.save()
    
    return redirect('cart')



#PAYMENTS VIEW
"""
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from decimal import Decimal

def initialize_payment(request):
    if request.method == 'POST':
        cart = get_object_or_404(Cart, session_key=request.session.session_key)
        total_amount = calculate_total(cart)
        amount_in_kobo = int(total_amount * 100)


        # Get user information from the form
        delivery_location = request.POST.get('delivery_location')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
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

        # Paystack API request data
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "amount": amount_in_kobo,
            "email": request.user.email if request.user.is_authenticated else "guest@example.com",
            "callback_url": request.build_absolute_uri(reverse('payment_callback')),
            "reference": f"cart_{request.session.session_key}_{total_amount}",  # Use a unique reference
        }

        # Initialize transaction with Paystack
        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            headers=headers,
            json=data
        )
        response_data = response.json()
        if response.status_code == 200:
            response_data = response.json()
            return redirect(response_data['data']['authorization_url'])
        else:
            # Handle error
            #return JsonResponse({'error': 'Failed to initialize payment'}, status=400)

            error_message = response_data.get('message', 'Unknown error occurred')
            return JsonResponse({
                'error': 'Payment initialization failed',
                'message': error_message,
                'details': response_data
            }, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

def payment_callback(request):
    # Verify the payment
    reference = request.GET.get('reference')
    if verify_payment(reference):
        cart = Cart.objects.filter(session_key=request.session.session_key).first()
        if cart:
            cart.delete()  # Example action: delete cart after successful payment
        return redirect('home')  # Redirect to the homepage
    else:
        # Payment failed
        return redirect('cart_view')

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
    # Implement the logic to calculate the total from the cart
    # This should match the logic in your cart view
    subtotal = Decimal('0.00')
    for item in cart.items.all():
        product = Product.objects.get(id=item.product.id)
        quantity = item.quantity
        total_price = product.price * quantity
        subtotal += total_price
    # Add tax and shipping, subtract discounts
    tax = subtotal * Decimal('0.05')  # Assuming 5% tax
    shipping = Decimal('10.00')  # Flat shipping rate
    discount = Decimal('0.00')  # Implement your discount logic
    
    return subtotal + tax + shipping - discount

"""










from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product
from django.db.models import Q

def product_list(request, category_id=None):

    #query = request.GET.get('query', '')
    #products = Product.objects.filter(name__icontains=query) if query else Product.objects.none()
    
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
"""
def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

"""

# views.py
from django.views.generic import ListView
from django.shortcuts import render
from .models import Product, Category
"""
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
"""
def category_products(request):
    #category = Category.objects.get(id=category_id)
    #products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'nav.html', {
        #'products': products,
        'categories': categories,
        #'current_category': category
    })


from django.shortcuts import render
from .models import Product   # Ensure this imports your Product model

def product_search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.none()
    context = {
        'products': products,
    }
    return render(request, 'your_template_name.html', context)



from django.http import JsonResponse
from django.db.models import Q
from .models import Product, SearchedProduct

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











# views.py
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse
from decimal import Decimal
import requests
from .models import Cart, Product, Order, OrderItem
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def initialize_payment(request):
    if request.method == 'POST':

        delivery_location = request.POST.get('delivery_location')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')

        # Ensure all required fields are provided
        if not all([delivery_location, name, phone_number]):
            #messages.error(request, "Please fill out all required fields.")
            return redirect('cart') 
        

        cart = get_object_or_404(Cart, session_key=request.session.session_key)
        total_amount = calculate_total(cart)
        amount_in_kobo = int(total_amount * 100)

        # Get user information from the form

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
        
        # Update order status
        order.paid = True
        order.status = 'processing'
        order.save()

        # Clear the cart
        Cart.objects.filter(session_key=order.session_key).delete()

        #return redirect('order_confirmation', order_id=order.id)
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
    # Implement the logic to calculate the total from the cart
    # This should match the logic in your cart view
    subtotal = Decimal('0.00')
    for item in cart.items.all():
        product = Product.objects.get(id=item.product.id)
        quantity = item.quantity
        total_price = product.price * quantity
        subtotal += total_price
    # Add tax and shipping, subtract discounts
    tax = subtotal * Decimal('0.05')  # Assuming 5% tax
    shipping = Decimal('10.00')  # Flat shipping rate
    discount = Decimal('0.00')  # Implement your discount logic
    
    return subtotal + tax + shipping - discount







# api/views.py
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import requests
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        order = self.get_object()
        order.status = 'completed'
        order.save()
        return Response({'status': 'order marked as completed'})

    def perform_create(self, serializer):
        order = serializer.save()
        send_order_to_external_site(order)

@receiver(post_save, sender=Order)
def order_created_signal(sender, instance, created, **kwargs):
    if created:
        send_order_to_external_site(instance)

def send_order_to_external_site(order):
    url = settings.EXTERNAL_SITE_URL
    serializer = OrderSerializer(order)
    try:
        response = requests.post(url, json=serializer.data)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to send order to external site: {e}")
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import Order
from .serializers import OrderSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


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
    #permission_classes = [IsAdminUser]

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
