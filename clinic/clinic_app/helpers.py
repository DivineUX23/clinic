from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart, Order, OrderItem, Profile, PaymentSettings, ShippingInfo, SenderAddress, ShippingInfo, SenderAddress
from django.conf import settings
import requests
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import uuid
from django.contrib import messages
from haversine import haversine, Unit
import logging
from django.core.cache import cache
from .models import Location
from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

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



def create_authenticated_order(request, form):
    location, created = Location.objects.get_or_create(
        formatted_address=form.cleaned_data['address'],
        defaults={'latitude': None, 'longitude': None}  
    )
    
    # Update user information
    user = request.user
    user.first_name = form.cleaned_data.get('first_name')
    user.last_name = form.cleaned_data.get('last_name')
    user.email = form.cleaned_data.get('email')
    user.save()

    # Update or create user profile
    profile, created = Profile.objects.get_or_create(user=user)
    profile.phone_number = form.cleaned_data.get('phone_number')
    profile.delivery_location = location
    profile.save()

    order = Order.objects.create(
        user=user,
        delivery_location=location,
        order_note=form.cleaned_data['order_note'],
        total_amount=calculate_total(get_object_or_404(Cart, user=user)),
        payment_reference=f"ORDER-{uuid.uuid4().hex[:8].upper()}",
        order_category=form.cleaned_data.get('order_category'),
        status='pending'
    )
    
    cart = get_object_or_404(Cart, user=user)
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            price=item.product.price,
            quantity=item.quantity
        )
    
    return order

"""
def get_or_create_guest_order(request):
    order_id = request.session.get('order_id')
    if order_id:
        order = Order.objects.filter(id=order_id, user__isnull=True).first()
        if order:
            return order
    
    order = Order.objects.create()
    request.session['order_id'] = order.id
    return order
"""

def create_session_order(request, form):
    with transaction.atomic():
        # Create or get the Location
        location, _ = Location.objects.get_or_create(
            formatted_address=form.cleaned_data['address'],
            defaults={'latitude': None, 'longitude': None}
        )

        # Create or update the Order
        order_id = request.session.get('order_id')
        if order_id:
            order = Order.objects.filter(id=order_id, user__isnull=True).first()
            if order:
                # Update existing order
                order.delivery_location = location
                order.order_note = form.cleaned_data['order_note']
                order.order_category = form.cleaned_data.get('order_category')
            else:
                # Create new order if existing one not found
                order = Order(delivery_location=location)
        else:
            # Create new order
            order = Order(delivery_location=location)

        # Update order fields
        order.total_amount = calculate_total(get_or_create_guest_cart(request))
        order.payment_reference = f"ORDER-{uuid.uuid4().hex[:8].upper()}"
        order.status = 'pending'
        order.order_note = form.cleaned_data['order_note']
        order.order_category = form.cleaned_data.get('order_category')
        order.save()

        # Store order ID in session
        request.session['order_id'] = order.id

        # Create or update OrderItems
        cart = get_or_create_guest_cart(request)
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                price=cart_item.product.price,
                quantity=cart_item.quantity
            )


        # Store guest user information in session
        request.session['guest_user'] = {
            'first_name': form.cleaned_data['first_name'],
            'last_name': form.cleaned_data['last_name'],
            'phone_number': form.cleaned_data['phone_number'],
            'email': form.cleaned_data['email'],
        }

    return order


def update_authenticated_order(order, shipment_data):
    shipping_info, created = ShippingInfo.objects.get_or_create(order=order)

    shipping_info.tracking_number = shipment_data['tracking_url']
    shipping_info.shipment_id = shipment_data['order_id']
    shipping_info.courier_name = shipment_data['courier']['name']
    shipping_info.courier_email = shipment_data['courier']['email']
    shipping_info.courier_phone = shipment_data['courier']['phone']
    shipping_info.shipment_status = shipment_data['status']
    shipping_info.shipping_fee = shipment_data['payment']['shipping_fee']
    shipping_info.package_weight = shipment_data['package_weight']
    shipping_info.tracking_url = shipment_data['tracking_url']
    shipping_info.shipment_date = shipment_data['date']
    shipping_info.save()

    order.paid = True
    order.status = 'confirmed'
    order.save()
    

#useless_now
def update_session_order(request, order, shipment_data):
    order.update({
        'shipment_id': shipment_data['order_id'],
        'courier_name': shipment_data['courier']['name'],
        'courier_email': shipment_data['courier']['email'],
        'courier_phone': shipment_data['courier']['phone'],
        'shipment_status': shipment_data['status'],
        'shipping_fee': str(shipment_data['payment']['shipping_fee']),
        'package_weight': str(shipment_data['package_weight']),
        'tracking_url': shipment_data['tracking_url'],
        'shipment_date': timezone.now().isoformat(),
        'paid': True,
        'status': 'confirmed',
    })
    request.session.modified = True


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



def find_closest_location(latitude, longitude):
    ref_location = (latitude, longitude)
    #locations = SenderAddress.objects.all()
    locations = SenderAddress.objects.exclude(formatted_address__isnull=True).exclude(formatted_address__exact='')
    print(locations)
    closest_location = min(
        locations, 
        key=lambda loc: haversine(ref_location, (loc.latitude, loc.longitude), unit=Unit.KILOMETERS))
    return closest_location


def get_shipping_rates(order, cart_items):
    url = "https://api.shipbubble.com/v1/shipping/fetch_rates"
    
    package_items = [
        {
            "name": item.product.name,
            "description": item.product.description[:100] if item.product.description else "Health related product from JollyLifeHealth",
            #"unit_weight": item.product.package_dimension.unit_weight if item.product.package_dimension.unit_weight else 1,
            "unit_weight": 1 if not hasattr(item.product, 'package_dimension') else item.product.package_dimension.unit_weight,
            "unit_amount": float(item.product.price),
            "quantity": item.quantity
        }
        for item in cart_items
    ]

    length = sum(item.product.package_dimension.length for item 
                 in cart_items if hasattr(item.product, 'package_dimension'))
    width = sum(item.product.package_dimension.width for item 
                in cart_items if hasattr(item.product, 'package_dimension'))
    height = sum(item.product.package_dimension.height for item 
                 in cart_items if hasattr(item.product, 'package_dimension'))


    users_address = create_or_get_address_code(order)

    if not isinstance(users_address, tuple) or len(users_address) < 3:
        return users_address  

    closest_location = find_closest_location(users_address[1], users_address[2])
    """
    ref_location = (users_address[1], users_address[2])

    locations = SenderAddress.objects.all()
    
    closest_location = min(
        locations, 
        key=lambda loc: haversine(ref_location, (loc.latitude, loc.longitude), unit=Unit.KILOMETERS))
    
    print(f"The closest location is: {closest_location}")
    """ 
    print(f"The closest location is: {closest_location}")

    sender_address = get_sender_address_code(closest_location) 

    if not isinstance(sender_address, int):
        return sender_address 
    
    data = {
        "sender_address_code": sender_address,
        "reciever_address_code": users_address, 
        "pickup_date": timezone.now().strftime("%Y-%m-%d"),
        "category_id": order.order_category if order.order_category else 99652979,
        "package_items": package_items,
        "package_dimension": {
            "length": length if length != 0 else 10,
            "width": width if width != 0 else 10,
            "height": height if height != 0 else 10,
        },
        "delivery_instructions": order.order_note if order.order_note else "Handle with care"
    }

    response = make_shipbubble_request(url, data)
    return response




def create_shipment(order):

    url = "https://api.shipbubble.com/v1/shipping/labels"
    
    data = {
        "request_token": order.shipping_info.request_token,
        "service_code": order.shipping_info.service_code,
        "courier_id": order.shipping_info.courier_id
    }

    print(f"--------------------{data}")
    response = make_shipbubble_request(url, data)
    #if response.get('status') == get_sender_address_code'success': {data['name']}"


    if response is None:
        return response



    if 'status' in response and response.get('status') == 'success':
        if 'data' in response and 'tracking_url' in response['data']:
            #if isinstance(order, dict):
                #order['tracking_number'] = response['data']['tracking_url']
            #else:
                #order.tracking_number = response['data']['tracking_url']
                #order.save()
            return response
        else:
            logger.error(f"Invalid response structure from Shipbubble API for order {order['id'] if isinstance(order, dict) else order.id}")
            return response
    else:
        logger.error(f"Shipment creation failed for order {order['id'] if isinstance(order, dict) else order.id}: {response.get('message')}")
        return response




def get_sender_address_code(sender):
    sender_code = cache.get('sender_address_code')
    if sender_code:
        print(f"\n\n chaced response------------------{sender_code}\n\n")
        return sender_code

    sender_address = SenderAddress.objects.get(id=sender.id)
    print(f"..............................................{sender_address.phone_number}")
    print(f"..............................................{sender_address.formatted_address}")

    if not sender_address:
        logger.error("No sender address found in the database")
        return {'status': 'error', 'message': f"No sender address found in the database"}

    url = "https://api.shipbubble.com/v1/shipping/address/validate"
    data = {
        "phone": sender_address.phone_number,
        "email": sender_address.admin.email,
        "name": f"{sender_address.admin.first_name} {sender_address.admin.last_name}",
        "address": sender_address.formatted_address
    }
    print(data)
    response = make_shipbubble_request(url, data)

    if 'status' in response and response.get('status') == 'success':
        if 'data' in response and 'address_code' in response['data']:
            sender_code = response['data']['address_code']
            cache.set('sender_address_code', sender_code, 60*60*24)
            return sender_code
        else:
            logger.error(f"Invalid response structure from Shipbubble API for order {data['name']}")
            return response
    else:
        logger.error(f"Error creating sender address: {response.get('message')}")
        return response



def create_or_get_address_code(order):
    #cache_key = f"address_code_{order['id'] if isinstance(order, dict) else order.id}"
    #cache_key = f"address_code_{order['payment_reference'] if isinstance(order, dict) else order.payment_reference}"
    cache_key = f"address_code_{order.payment_reference}"

    address_code = cache.get(cache_key)
    if address_code:
        print(f"\n\n chaced user------------------{address_code}\n\n")
        return address_code

    url = "https://api.shipbubble.com/v1/shipping/address/validate"


    if order.user:  # Authenticated order
        data = {
            "phone": str(order.user.profile.phone_number),
            "email": str(order.user.email),
            "name": f"{str(order.user.first_name)} {str(order.user.last_name)}",
            "address": str(order.delivery_location.formatted_address)
        }
    else:  # Session order
        guest_info = order.request.session.get('guest_user', {}) if hasattr(order, 'request') else {}
        data = {
            "phone": str(guest_info.get('phone_number', '')),
            "email": str(guest_info.get('email', '')),
            "name": f"{str(guest_info.get('first_name', ''))} {str(guest_info.get('last_name', ''))}",
            "address": str(order.delivery_location.formatted_address)
        }


    print(data)

    response = make_shipbubble_request(url, data)
    if 'status' in response and response.get('status') == 'success':
        if 'data' in response and 'address_code' in response['data']:
            address_code = response['data']['address_code']
            cache.set(cache_key, address_code, 60*60)

            if hasattr(order, 'delivery_location') and order.delivery_location:
                order.delivery_location.latitude = response['data'].get('latitude')
                order.delivery_location.longitude = response['data'].get('longitude')
                order.delivery_location.save()
            
            return (address_code, 
                    response['data']['latitude'], 
                    response['data']['longitude'])
        else:
            logger.error(f"Invalid response structure from Shipbubble API for order {data['name']}")
            return response
    else:
        logger.error(f"Error creating address for order {data['name']}: {response.get('message')}")
        return response



def filter_health_medical_categories(all_categories):
    #all_categories = api_response.get('data', [])
    filtered_categories = [category for category in all_categories if "health" in category['category'].lower() or "medical" in category['category'].lower()]
    return filtered_categories

def get_categories():
    url = "https://api.shipbubble.com/v1/shipping/labels/categories"
    response = make_shipbubble_request(url, method='GET')
    api_response = response.get('data', [])
    filtered_categories = filter_health_medical_categories(api_response)
    print(filtered_categories)
    return filtered_categories


def update_profile(profile, form_data):
    if profile.phone_number != form_data['phone_number']:
        profile.phone_number = form_data['phone_number']
    if profile.email != form_data['email']:
        profile.email = form_data['email']
    profile.save()



def make_shipbubble_request(url, data=None, method='POST'):
    headers = {
        "Authorization": f"Bearer {settings.SHIPBUBBLE_API_KEY}",
        "Content-Type": "application/json",
    }
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        else:
            print(f"------------{data}")

            response = requests.post(url, headers=headers, json=data)
            
            print(f"HERE WE GO AGAIN------11111--------{response.json()}")
            return(response.json())

        response.raise_for_status()
        print(response.json())
        return response.json()
    
    except requests.RequestException as e:
        print(f"HERE WE GO AGAIN------2222222--------{e}")
        logger.error(f"Shipbubble API error: {str(e)}")
        return {'status': 'error', 'message': str(e)}


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










def send_admin_notification(order, shipment_success):
    subject = f"New Order #{order.id} - Shipment {'Success' if shipment_success else 'Failed'}"
    
    # Get product details
    product_details = "\n".join([
        f"- {item.product.name}: {item.quantity} x ${item.price} = ${item.get_cost()}"
        for item in order.items.all()
    ])

    message = f"""
    A new order has been placed and paid for.

    Order Details:
    - Order ID: {order.id}
    - Customer: {order.user.get_full_name() if order.user else 'Guest'}
    - Total Amount: ${order.total_amount}
    - Status: {order.status}
    - Order Category: {order.order_category}
    - Order Note: {order.order_note or 'N/A'}

    Products Purchased:
    {product_details}

    Shipment Status: {'Success' if shipment_success else 'Failed'}

    {'The shipment was created successfully.' if shipment_success else 'The shipment creation failed. Manual intervention may be required.'}

    {'Shipping Information:' if shipment_success else 'Action required:'}
    """

    if shipment_success and hasattr(order, 'shipping_info'):
        shipping_info = order.shipping_info
        message += f"""
    - Shipment ID: {shipping_info.shipment_id}
    - Tracking Number: {shipping_info.tracking_number}
    - Courier: {shipping_info.courier_name}
    - Courier Contact: {shipping_info.courier_phone} | {shipping_info.courier_email}
    - Shipping Cost: ${shipping_info.shipping_cost}
    - Package Weight: {shipping_info.package_weight} kg
    - Tracking URL: {shipping_info.tracking_url}
    - Shipment Date: {shipping_info.shipment_date}
    """
    else:
        message += """
    - Please manually create the shipment for this order.
    - Contact the customer to provide updates.
    """

    message += """
    Please log in to the admin panel for more details and to take necessary actions.
    """

    from_email = settings.DEFAULT_FROM_EMAIL

    admin_users = User.objects.filter(is_superuser=True)
    recipient_list = [admin.email for admin in admin_users if admin.email]

    if not recipient_list:
        messages.error(f"Failed to send admin notification email: {e}")
        return

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        messages.error(f"Failed to send admin notification email: {e}")



def send_user_notification(order, success):
    if success:
        subject = f"Your Order #{order.id} Has Been Shipped"
        message = f"""
        Dear {order.user.get_full_name() if order.user else 'Valued Customer'},

        Your order (#{order.id}) has been successfully processed and shipped.

        Tracking Number: {order.shipping_info.tracking_number}
        Courier Name: {order.shipping_info.courier_name}
        Courier: {order.shipping_info.courier_name}
        Courier Contact: {order.shipping_info.courier_phone} | {order.shipping_info.courier_email}
        Shipment Date: {order.shipping_info.shipment_date}

        Estimated Delivery: Within 1 working day.

        You can track your package using this link: {order.shipping_info.tracking_url}

        Thank you for your purchase!
        """
    else:
        subject = f"Issue with Your Order #{order.id}"
        message = f"""
        Dear {order.user.get_full_name() if order.user else 'Valued Customer'},

        We're writing to inform you that there was an issue processing the shipment for your order (#{order.id}).

        Our team has been notified and is working to resolve this issue. We will contact you shortly with more information.

        We apologize for any inconvenience this may cause.

        If you have any questions, please don't hesitate to contact our customer support.

        Thank you for your patience and understanding.
        """

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [order.user.email if order.user else order.email]
    
    #send_mail(subject, message, from_email, recipient_list)

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        messages.error(f"Failed to send admin notification email: {e}")
