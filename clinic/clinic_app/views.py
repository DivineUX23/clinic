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


# Create your views here.
def home(request):
    new_arrivals = Product.objects.filter(category='new_arrival')
    most_popular = Product.objects.filter(category='most_popular')
    return render(request, 'home.html', {
        'new_arrivals': new_arrivals,
        'most_popular': most_popular
    })



def category(request):
    return render(request, 'category.html', {})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:5]
    context = {
        'product': product,
        'related_products': related_products,
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
        
    tax = subtotal * Decimal('0.05')  # Assuming 5% tax
    shipping = Decimal('1000.00')  # Flat shipping rate
    discount = Decimal('0.00')  # You can implement discounts later
    total = subtotal + tax + shipping - discount
    
    context = {
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

import requests
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.http import JsonResponse
from decimal import Decimal

def initialize_payment(request):
    if request.method == 'POST':
            # Get cart and calculate total
        cart = get_object_or_404(Cart, session_key=request.session.session_key)
        total_amount = calculate_total(cart)

        # Paystack requires amount in kobo (multiply by 100)
        amount_in_kobo = int(total_amount * 100)

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
