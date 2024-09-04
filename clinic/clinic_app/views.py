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

# Create your views here.
def home(request):
    new_arrivals = Product.objects.filter(category='new_arrival')
    most_popular = Product.objects.filter(category='most_popular')
    return render(request, 'home.html', {
        'new_arrivals': new_arrivals,
        'most_popular': most_popular
    })



def cart(request):
    cart = get_cart(request)
    return render(request, 'cart.html', {'cart': cart})


def get_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def add_to_cart(request):
    if request.method == 'POST':
        
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)
        print(f"Product ID: {product_id}, Quantity: {quantity}")

        cart = get_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity = F('quantity') + quantity
        cart_item.save()

        return JsonResponse({'success': True, 'cart_quantity': cart.items.count()})
    return JsonResponse({'success': False}, status=400)




"""
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        # Check if the product is already in the cart
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return JsonResponse({'success': True, 'cart_item_id': cart_item.id, 'quantity': cart_item.quantity})
    
    return JsonResponse({'success': False}, status=400)


def add_to_cart(request):
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quantity=quantity)
        return JsonResponse({'success': True, 'cart_quantity': len(cart)})
    return JsonResponse({'success': False}, status=400)
"""
