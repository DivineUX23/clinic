"""
{
    "status": "success",
    "message": "Retrieved successfully",
    "data": {
        "request_token": "8e5184aa2b9dac2219bbf6270ea23cf5a7f22eab7119c508da683bf5d66c7235",
        "couriers": [
            {
                "courier_id": "test_1_courier",
                "courier_name": "Bubble Express",
                "courier_image": "https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png",
                "service_code": "test_1_courier",
                "insurance": {
                    "code": "not available",
                    "fee": 0
                },
                "discount": {
                    "percentage": 10,
                    "symbol": "%",
                    "discounted": 120
                },
                "service_type": "pickup",
                "waybill": false,
                "on_demand": true,
                "is_cod_available": false,
                "tracking_level": 7,
                "ratings": 3,
                "votes": 1,
                "connected_account": false,
                "rate_card_amount": 1680.3,
                "rate_card_currency": "NGN",
                "pickup_eta": "Within 24 Hours",
                "pickup_eta_time": "2024-10-05 11:11:01",
                "dropoff_station": null,
                "pickup_station": null,
                "delivery_eta": "Same day delivery",
                "delivery_eta_time": "2024-10-04 23:11:01",
                "info": null,
                "currency": "NGN",
                "vat": 90,
                "total": 1680.3,
                "tracking": {
                    "bars": 4,
                    "label": "Good"
                }
            },
            {
                "courier_id": "test_2_courier",
                "courier_name": "Richard Express",
                "courier_image": "https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png",
                "service_code": "test_2_courier",
                "insurance": {
                    "code": "not available",
                    "fee": 0
                },
                "discount": {
                    "percentage": 5,
                    "symbol": "%",
                    "discounted": 100
                },
                "service_type": "pickup",
                "waybill": true,
                "on_demand": true,
                "is_cod_available": true,
                "tracking_level": 7,
                "ratings": 3,
                "votes": 1,
                "connected_account": false,
                "rate_card_amount": 2600.5,
                "rate_card_currency": "NGN",
                "pickup_eta": "Within 24 Hours",
                "pickup_eta_time": "2024-10-05 11:11:01",
                "dropoff_station": null,
                "pickup_station": null,
                "delivery_eta": "Between 1 - 4 business working days",
                "delivery_eta_time": "2024-10-07 11:11:01",
                "info": null,
                "currency": "NGN",
                "vat": 150,
                "total": 2600.5,
                "tracking": {
                    "bars": 4,
                    "label": "Good"
                }
            },
            {
                "courier_id": "test_3_courier",
                "courier_name": "Millie Express",
                "courier_image": "https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png",
                "service_code": "test_3_courier",
                "insurance": {
                    "code": "not available",
                    "fee": 0
                },
                "discount": {
                    "percentage": 12,
                    "symbol": "%",
                    "discounted": 202
                },
                "service_type": "dropoff",
                "waybill": true,
                "on_demand": true,
                "is_cod_available": false,
                "tracking_level": 7,
                "ratings": 3,
                "votes": 1,
                "connected_account": false,
                "rate_card_amount": 2232.42,
                "rate_card_currency": "NGN",
                "pickup_eta": "Within 24 Hours",
                "pickup_eta_time": "2024-10-05 11:11:01",
                "dropoff_station": {
                    "name": "Astroworld park",
                    "address": "No 15 Walker NBA YoungBoy Street",
                    "country": "Nigeria",
                    "phone": null
                },
                "pickup_station": {
                    "name": "Astroworld park",
                    "address": "No 15 Walker NBA YoungBoy Street",
                    "phone": null
                },
                "delivery_eta": "Between 12 - 48 Hours",
                "delivery_eta_time": "2024-10-07 11:11:01",
                "info": null,
                "currency": "NGN",
                "vat": 126,
                "total": 2232.42,
                "tracking": {
                    "bars": 4,
                    "label": "Good"
                }
            }
        ],
        "fastest_courier": {
            "courier_id": "test_1_courier",
            "courier_name": "Bubble Express",
            "courier_image": "https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png",
            "service_code": "test_1_courier",
            "insurance": {
                "code": "not available",
                "fee": 0
            },
            "discount": {
                "percentage": 10,
                "symbol": "%",
                "discounted": 120
            },
            "service_type": "pickup",
            "waybill": false,
            "on_demand": true,
            "is_cod_available": false,
            "tracking_level": 7,
            "ratings": 3,
            "votes": 1,
            "connected_account": false,
            "rate_card_amount": 1680.3,
            "rate_card_currency": "NGN",
            "pickup_eta": "Within 24 Hours",
            "pickup_eta_time": "2024-10-05 11:11:01",
            "dropoff_station": null,
            "pickup_station": null,
            "delivery_eta": "Same day delivery",
            "delivery_eta_time": "2024-10-04 23:11:01",
            "info": null,
            "currency": "NGN",
            "vat": 90,
            "total": 1680.3,
            "tracking": {
                "bars": 4,
                "label": "Good"
            }
        },
        "cheapest_courier": {
            "courier_id": "test_1_courier",
            "courier_name": "Bubble Express",
            "courier_image": "https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png",
            "service_code": "test_1_courier",
            "insurance": {
                "code": "not available",
                "fee": 0
            },
            "discount": {
                "percentage": 10,
                "symbol": "%",
                "discounted": 120
            },
            "service_type": "pickup",
            "waybill": false,
            "on_demand": true,
            "is_cod_available": false,
            "tracking_level": 7,
            "ratings": 3,
            "votes": 1,
            "connected_account": false,
            "rate_card_amount": 1680.3,
            "rate_card_currency": "NGN",
            "pickup_eta": "Within 24 Hours",
            "pickup_eta_time": "2024-10-05 11:11:01",
            "dropoff_station": null,
            "pickup_station": null,
            "delivery_eta": "Same day delivery",
            "delivery_eta_time": "2024-10-04 23:11:01",
            "info": null,
            "currency": "NGN",
            "vat": 90,
            "total": 1680.3,
            "tracking": {
                "bars": 4,
                "label": "Good"
            }
        },
        "checkout_data": {
            "ship_from": {
                "name": "Burger King",
                "phone": "+2348115467102",
                "email": "sdsfsfs997@gmail.com",
                "address": "No 5 David Effiong Attah street karu site, Abuja Municipal, Abuja, Nigeria"
            },
            "ship_to": {
                "name": "Burger King",
                "phone": "+2348115467102",
                "email": "sdsfsfs997@gmail.com",
                "address": "No 5 David Effiong Attah street karu site, Abuja Municipal, Abuja, Nigeria"
            },
            "currency": "NGN",
            "package_amount": 310000,
            "package_weight": 4,
            "pickup_date": "October 4th 2024",
            "is_invoice_required": false
        }
    }
}{
    "sender_address_code":12670398,
    "reciever_address_code":12670398,
    "pickup_date":"2023-06-02",
    "category_id":57487393,
    "package_items":[
        {
            "name":"Jameson",
            "description":"This drink is lit",
            "unit_weight":1,
            "unit_amount":5000,
            "quantity":2
        },
        {
            "name":"Hennesy",
            "description":"XO na champion",
            "unit_weight":1,
            "unit_amount":150000,
            "quantity":2
        }
    ],
    "package_dimension":{
        "length":12,
        "width":10,
        "height":10
    },
    "delivery_instructions":"Please provide additional instructions for your package"
}






























def shipping_rates(request):
    if request.method == 'POST':
        # Get form data
        street_no = request.POST.get('street_no', '').strip()
        street = request.POST.get('street', '').strip()
        country_id = request.POST.get('country')
        state_id = request.POST.get('state')
        city_id = request.POST.get('city')
        postal_code = request.POST.get('postal_code', '').strip()
        name = request.POST.get('name', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        email = request.POST.get('email', '').strip()
        category = request.POST.get('category', '').strip()
        order_note = request.POST.get('order_note')

        # Validate required fields
        if not all([street, country_id, state_id, city_id, name, phone_number]):
            messages.error(request, "Please fill out all required fields.")
            return redirect('cart')

        # Validate name and phone number
        if not re.match(r'^[a-zA-Z\s]+$', name):
            messages.error(request, "Name should only contain letters and spaces.")
            return redirect('cart')

        if not re.match(r'^\d{10,14}$', phone_number):
            messages.error(request, "Please enter a valid phone number (10-14 digits).")
            return redirect('cart')

        # Handle location for authenticated users
        if request.user.is_authenticated:
            profile = request.user.profile
            
            # Check if user has a location
            if profile.delivery_location:
                location = profile.delivery_location
                # Update location if it's different
                if (location.street_no != street_no or
                    location.street != street or
                    location.country_id != int(country_id) or
                    location.state_id != int(state_id) or
                    location.city_id != int(city_id) or
                    location.postal_code != postal_code):
                    
                    location.street_no = street_no
                    location.street = street
                    location.country_id = country_id
                    location.state_id = state_id
                    location.city_id = city_id
                    location.postal_code = postal_code
                    location.save()
            else:
                # Create new location if user doesn't have one
                location = Location.objects.create(
                    street_no=street_no,
                    street=street,
                    country_id=country_id,
                    state_id=state_id,
                    city_id=city_id,
                    postal_code=postal_code
                )
                profile.delivery_location = location

            # Update profile information
            if profile.phone_number != phone_number:
                profile.phone_number = phone_number
            if profile.email != email:
                profile.email = email
            profile.save()

            cart = get_object_or_404(Cart, user=request.user)
        else:
            # For non-authenticated users, always create a new location
            location = Location.objects.create(
                street_no=street_no,
                street=street,
                country_id=country_id,
                state_id=state_id,
                city_id=city_id,
                postal_code=postal_code
            )
            cart = get_or_create_guest_cart(request)

        # Calculate total amount
        total_amount = calculate_total(cart)

        # Generate a random payment reference
        payment_reference = f"ORDER-{uuid.uuid4().hex[:8].upper()}"

        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key if not request.user.is_authenticated else None,
            delivery_location=location,
            name=name,
            phone_number=phone_number,
            email=email,
            order_note=order_note,
            total_amount=total_amount,
            payment_reference=payment_reference,
            status='pending',
            category=category
        )

        # Create OrderItems
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )

        # Get shipping rates
        shipping_rates = get_shipping_rates(order, cart.items.all())

        categories = get_categories()

        context = {
            'couriers': shipping_rates["data"]["couriers"],
            'fastest_courier': shipping_rates["data"]["fastest_courier"],
            'cheapest_courier': shipping_rates["data"]["cheapest_courier"],
            'checkout_data': shipping_rates["data"]["checkout_data"],
            'categories': categories
        }
        return render(request, 'couriors.html', context)

    # If not POST, redirect to cart
    return redirect('cart')
    #once button clicks striaght to paystack



def initialize_payment(request, order_id):
    if request.method == 'POST':

        chosen_rate = request.POST.get('chosen_rate', '').strip()
        chosen_category = request.POST.get('chosen_category', '').strip()        
       
        if not chosen_rate:
            messages.error(request, "Please choose a shipping method.")
            return redirect('couriors.html')
                
        order = get_object_or_404(Order, id=order_id)
        order.shipping_method = chosen_rate['courier_name']
        order.shipping_cost = Decimal(chosen_rate['total'])
        order.category = chosen_category
        order.save()

        amount_in_kobo = int((order.total_amount +  order.shipping_cost) * 100)

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
        
        # Create shipment
        create_shipment(order)


        order.paid = True
        order.status = 'processing'
        order.save()

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











def get_shipping_rates(order, cart_items):
    url = "https://api.shipbubble.com/v1/shipping/fetch_rates"
    headers = {
        "Authorization": f"Bearer {settings.SHIPBUBBLE_API_KEY}",
        "Content-Type": "application/json",
    }
    
    # Prepare package items
    package_items = [
        {
            "name": item.product.name,
            "description": item.product.description[:100],
            "unit_weight": 1,
            "unit_amount": float(item.product.price),
            "quantity": item.quantity
        }
        for item in cart_items
    ]

    data = {
        "sender_address_code": get_sender_address_code(),
        "reciever_address_code": create_or_get_address_code(order),
        "pickup_date": datetime.now().strftime("%Y-%m-%d"),
        "category_id": order.category,  # Assume "accessories" category, adjust as needed {{url}}/shipping/labels/categories
        "package_items": package_items,
        "package_dimension": {
            "length": 10,
            "width": 10,
            "height": 10
        },
        "delivery_instructions": order.order_note
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['data']['couriers'] #users will choose couriers, create UI
    else:
        # Handle error
        return []


def create_shipment(order):
    url = "https://api.shipbubble.com/v1/shipping/shipments"
    headers = {
        "Authorization": f"Bearer {settings.SHIPBUBBLE_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "sender_address_code": get_sender_address_code(),
        "reciever_address_code": create_or_get_address_code(order.delivery_location),
        "courier_id": order.shipping_method,
        "package_items": [
            {
                "name": item.product.name,
                "description": item.product.description[:100],
                "unit_weight": 1,  # Assume 1kg per item, adjust as needed
                "unit_amount": float(item.price),
                "quantity": item.quantity
            }
            for item in order.items.all()
        ],
        "package_dimension": {
            "length": 10,
            "width": 10,
            "height": 10
        },
        "delivery_instructions": order.order_note or "Handle with care"
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        shipment_data = response.json()['data']
        order.tracking_number = shipment_data['tracking_number']
        order.save()
    else:
        # Handle error
        pass



from django.core.cache import cache
import requests
from django.conf import settings

def get_sender_address_code():
    # Check if the sender address code is in cache
    sender_code = cache.get('sender_address_code')
    if sender_code:
        return sender_code

    # If not in cache, create or get the code from Shipbubble
    #url = "https://api.shipbubble.com/v1/shipping/address"
    url = "https://api.shipbubble.com/v1/shipping/address/validate"

    headers = {
        "Authorization": f"Bearer {settings.SHIPBUBBLE_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "street_no": settings.BUSINESS_STREET_NO,
        "street": settings.BUSINESS_STREET,
        "country": settings.BUSINESS_COUNTRY,
        "state": settings.BUSINESS_STATE,
        "city": settings.BUSINESS_CITY,
        "postal_code": settings.BUSINESS_POSTAL_CODE,
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        sender_code = response.json()['data']['address_code']
        # Cache the sender code for future use (cache for 1 day)
        cache.set('sender_address_code', sender_code, 60*60*24)
        return sender_code
    else:
        # Handle error - you might want to log this
        print(f"Error creating sender address: {response.text}")
        return None



def create_or_get_address_code(order):
    # Create a unique key for this order
    cache_key = f"address_code_{order.id}"

    # Check if the address code is in cache
    address_code = cache.get(cache_key)
    if address_code:
        return address_code

    # If not in cache, create or get the code from Shipbubble
    url = "https://api.shipbubble.com/v1/shipping/address/validate"


    headers = {
        "Authorization": f"Bearer {settings.SHIPBUBBLE_API_KEY}",
        "Content-Type": "application/json",
    }

    delivery_address = get_object_or_404(Location, id = order.delivery_location)
    data = {
        "phone": order.phone_number,
        "email": order.email,
        "name": order.name,
        "address": delivery_address
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        address_code = response.json()['data']['address_code']
        # Cache the address code for future use (cache for 1 hour)
        cache.set(cache_key, address_code, 60*60)
        return address_code
    else:
        # Handle error - you might want to log this
        print(f"Error creating address: {response.text}")
        return None





def get_categories():
    url = "https://api.shipbubble.com/v1/shipping/labels/categories"
    headers = {
        "Authorization": f"Bearer {settings.SHIPBUBBLE_API_KEY}",
        "Content-Type": "application/json",
    }
    
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        # Handle error
        return []














#---------------------

import requests
from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import re
import uuid
"""