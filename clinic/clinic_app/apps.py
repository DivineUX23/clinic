from django.apps import AppConfig


class ClinicAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic_app'


"""
{"status":"success","message":"Retrieved successfully","data":{"request_token":"8c656ce8757eeddb34aced59f1518161e7c3a7158a5941c8f83c74f5b67bf727","couriers":
                                                               
            [{"courier_id":"test_2_courier",
              "courier_name":"Richard Express",     
              "courier_image":"",
              "service_code":"test_2_courier",
              "insurance":{"code":"not available",
                           "fee":0},
              "discount":{"percentage":5,
                          "symbol":"%",
                          "discounted":50},
              "service_type":"pickup",
              "waybill":true,
              "on_demand":true,7
              "is_cod_available":true,
              "tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":1450.25,
              "rate_card_currency":"NGN",
              "pickup_eta":"Within 24 Hours",
              "pickup_eta_time":"2024-10-09 14:57:48",
              "dropoff_station":null,
              "pickup_station":null,
              "delivery_eta":"Between 1 - 4 business working days","delivery_eta_time":"2024-10-11 14:57:48",
              "info":null,"currency":"NGN","vat":75,
              "total":1450.25,"tracking":{"bars":4,
                                          "label":"Good"}
                                          },

             
             {"courier_id":"test_3_courier","courier_name":"Millie Express","courier_image":"https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png","service_code":"test_3_courier","insurance":{"code":"not available","fee":0},"discount":{"percentage":12,"symbol":"%","discounted":101},"service_type":"dropoff","waybill":true,"on_demand":true,"is_cod_available":false,"tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":1266.21,"rate_card_currency":"NGN","pickup_eta":"Within 24 Hours","pickup_eta_time":"2024-10-09 14:57:48","dropoff_station":{"name":"Astroworld park","address":"No 15 Walker NBA YoungBoy Street","country":"Nigeria","phone":null},"pickup_station":{"name":"Astroworld park","address":"No 15 Walker NBA YoungBoy Street","phone":null},"delivery_eta":"Between 12 - 48 Hours","delivery_eta_time":"2024-10-11 14:57:48","info":null,"currency":"NGN","vat":63,"total":1266.21,"tracking":{"bars":4,"label":"Good"}},
             
             {"courier_id":"test_1_courier","courier_name":"Bubble Express","courier_image":"https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png","service_code":"test_1_courier","insurance":{"code":"not available","fee":0},"discount":{"percentage":10,"symbol":"%","discounted":60},"service_type":"pickup","waybill":false,"on_demand":true,"is_cod_available":false,"tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":990.15,"rate_card_currency":"NGN","pickup_eta":"Within 24 Hours","pickup_eta_time":"2024-10-09 14:57:48","dropoff_station":null,"pickup_station":null,"delivery_eta":"Same day delivery","delivery_eta_time":"2024-10-09 02:57:48","info":null,"currency":"NGN","vat":45,"total":990.15,"tracking":{"bars":4,"label":"Good"}}],
            

            "fastest_courier":{"courier_id":"test_1_courier","courier_name":"Bubble Express","courier_image":"https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png","service_code":"test_1_courier","insurance":{"code":"not available","fee":0},"discount":{"percentage":10,"symbol":"%","discounted":60},"service_type":"pickup","waybill":false,"on_demand":true,"is_cod_available":false,"tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":990.15,"rate_card_currency":"NGN","pickup_eta":"Within 24 Hours","pickup_eta_time":"2024-10-09 14:57:48","dropoff_station":null,"pickup_station":null,"delivery_eta":"Same day delivery","delivery_eta_time":"2024-10-09 02:57:48","info":null,"currency":"NGN","vat":45,"total":990.15,"tracking":{"bars":4,"label":"Good"}},
            
            "cheapest_courier":{"courier_id":"test_1_courier","courier_name":"Bubble Express","courier_image":"https://res.cloudinary.com/delivry/image/upload/v1646216432/courier_images/bubble_delivery_aojavr.png","service_code":"test_1_courier","insurance":{"code":"not available","fee":0},"discount":{"percentage":10,"symbol":"%","discounted":60},"service_type":"pickup","waybill":false,"on_demand":true,"is_cod_available":false,"tracking_level":7,"ratings":3,"votes":1,"connected_account":false,"rate_card_amount":990.15,"rate_card_currency":"NGN","pickup_eta":"Within 24 Hours","pickup_eta_time":"2024-10-09 14:57:48","dropoff_station":null,"pickup_station":null,"delivery_eta":"Same day delivery","delivery_eta_time":"2024-10-09 02:57:48","info":null,"currency":"NGN","vat":45,"total":990.15,"tracking":{"bars":4,"label":"Good"}},
            
            "checkout_data":{"ship_from":{"name":"Mather Osas","phone":"+2347067239473","email":"Sam@gmail.com","address":"1, Ugbowo, Benin City, Edo State, 4444, Nigeria"},"ship_to":{"name":"Mather Osas","phone":"+2347067239473","email":"Sam@gmail.com","address":"1, Ugbowo, Benin City, Edo State, 4444, Nigeria"},"currency":"NGN","package_amount":4000,"package_weight":2,"pickup_date":"October 8th 2024","is_invoice_required":false}}}

"""















{
    "status": "success",
    "message": "Validation successful",
    "data": {
        "address_code": 32660723,
        "address": "No 5 David Effiong Attah street karu site, Abuja Municipal, Abuja, Nigeria",
        "name": "Burger King",
        "email": "sdsfsfs997@gmail.com",
        "street_no": "1",
        "street": "Clement Attah Street",
        "phone": "+2348115467102",
        "formatted_address": "Clement Attah St, Ado 900101, Federal Capital Territory, Nigeria",
        "country": "Nigeria",
        "country_code": "NG",
        "city": "Abuja Municipal Area Council",
        "city_code": "AMAC",
        "state": "Federal Capital Territory",
        "state_code": "Federal Capital Territory",
        "postal_code": "900101",
        "latitude": 9.0335314,
        "longitude": 7.5834764
    }
}












"""
shipment_order_id

This is my current view regarding related info: "


def initialize_payment(request):
if request.method == 'POST':

form = OrderForm(request.POST)
print(form)
if form.is_valid():

formatted_address = form.cleaned_data['address']

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
formatted_address=formatted_address
)
cart = get_or_create_guest_cart(request)

total_amount = calculate_total(cart)
payment_reference = f"ORDER-{uuid.uuid4().hex[:8].upper()}"
order = create_order(request, location, form.cleaned_data, total_amount, payment_reference)
shipping_rates = get_shipping_rates(order, cart.items.all())
print(f"\n\n shipping_rates user------------------'{shipping_rates}'\n\n")

if shipping_rates is None:
messages.error(request, f"Shipbubble Error: Error accessing riders in your location, try again")
return redirect('cart')


if 'status' in shipping_rates and shipping_rates.get('status') == 'success':

if 'data' in shipping_rates:
shipping_rates = shipping_rates.get('data', {})
else:
#messages.error(request, f"{shipping_rates.get('message')}")
messages.error(request, f"Shipbubble Error: {shipping_rates.get('message')}")
return redirect('cart')
elif 'status' in shipping_rates and shipping_rates.get('status') == 'error':

#messages.error(request, f"{shipping_rates.get('message')}")
messages.error(request, f"Shipbubble Error: {shipping_rates.get('message')}")
return redirect('cart')
else:
#messages.error(request, f"{shipping_rates.get('message')}")
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
order = get_object_or_404(Order, payment_reference=reference)

# Create shipment
shipment_created = create_shipment(order)
print(shipment_created)

if shipment_created is None:
messages.error(request, "Failed to retrieve shipping rates.")
return redirect('cart')


if 'status' in shipment_created and shipment_created.get('status') == 'success':

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



users_address = create_or_get_address_code(order)

if not isinstance(users_address, tuple) or len(users_address) < 3:
return users_address


ref_location = (users_address[1], users_address[2])

locations = SenderAddress.objects.all()

closest_location = min(
locations,
key=lambda loc: haversine(ref_location, (loc.latitude, loc.longitude), unit=Unit.KILOMETERS))

print(f"The closest location is: {closest_location}")

sender_address = get_sender_address_code(closest_location)

if not isinstance(sender_address, int):
return sender_address

data = {
"sender_address_code": sender_address,
"reciever_address_code": users_address,
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

if response.get('status') == 'error':
if '422' in response["message"]:
return {'status': 'error', 'message': f"Error accessing riders in your location, try again"}
elif '400' in response["message"]:
return {'status': 'error', 'message': f"Error accessing riders in your location."}
return response

request_token


def create_shipment(order):


url = "https://api.shipbubble.com/v1/shipping/labels"

data = {
"request_token": order.request_token,
"service_code": order.service_code,
"courier_id": order.courier_id
}

print(f"--------------------{data}")
response = make_shipbubble_request(url, data)
#if response.get('status') == get_sender_address_code'success': {data['name']}"


if response is None:
return response


if 'status' in response and response.get('status') == 'success':

if 'data' in response and 'tracking_url' in response['data']:
order.tracking_number = response['data']['tracking_url']
order.save()
return response
else:
logger.error(f"Invalid response structure from Shipbubble API for order {order.id}")
return response
else:
logger.error(f"Shipment creation failed for order {order.id}: {response.get('message')}")
return response




def get_sender_address_code(sender):
sender_code = cache.get('sender_address_code')
if sender_code:
print(f"\n\n chaced response------------------{sender_code}\n\n")
return sender_code

sender_address = SenderAddress.objects.get(id=sender.id)
print(f"..............................................{sender_address.phone_number}")
print(f"..............................................{sender_address.email}")
print(f"..............................................{sender_address.formatted_address}")

if not sender_address:
logger.error("No sender address found in the database")
return {'status': 'error', 'message': f"No sender address found in the database"}

url = "https://api.shipbubble.com/v1/shipping/address/validate"
data = {
"phone": sender_address.phone_number,
"email": sender_address.email,
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
elif response.get('status') == 'error':
if '422' in response["message"]:
return {'status': 'error', 'message': f"Error Validating senders details, Contact us to resolve issue"}
elif '400' in response["message"]:
return {'status': 'error', 'message': f"Error Validating senders address, Contact us to resolve issue"}
else:
logger.error(f"Error creating sender address: {response.get('message')}")
return {'status': 'error', 'message': f"Error Validating senders data, Contact us to resolve issue"}



def create_or_get_address_code(order):
cache_key = f"address_code_{order.id}"
address_code = cache.get(cache_key)
if address_code:
print(f"\n\n chaced user------------------{address_code}\n\n")
return address_code

url = "https://api.shipbubble.com/v1/shipping/address/validate"

delivery_address = order.delivery_location

#data = {"phone": "07067239473", response.sta"email": "Sam@gmail.com", "name": "Mather Osas", "address": "1, Ugbowo, Benin City, Edo State, 4444, Nigeria"}
data = {
"phone": str(order.phone_number),
"email": str(order.email),
"name": f"{str(order.first_name)} {str(order.last_name)}",
"address": str(delivery_address.formatted_address)
}
print(data)

response = make_shipbubble_request(url, data)
print(f"\n\n bubblw response------------------{response}\n\n")


if 'status' in response and response.get('status') == 'success':
if 'data' in response and 'address_code' in response['data']:
address_code = response['data']['address_code']
cache.set(cache_key, address_code, 60*60)
return (address_code, response['data']['latitude'], response['data']['longitude'])
else:
logger.error(f"Invalid response structure from Shipbubble API for order {data['name']}")
return response
elif response.get('status') == 'error':
error_message = response.get("message", "Unknown error")
if '422' in response["message"]:
return {'status': 'error', 'message': f"Error Validating your details, ensure your details are correct"}
elif '400' in response["message"]:
return {'status': 'error', 'message': f"Error Validating your address, ensure your address is correct"}
else:
return {'status': 'error', 'message': error_message}

else:
logger.error(f"Error creating address for order {data['name']}: {response.get('message')}")
return {'status': 'error', 'message': f"Error Validating your data, ensure your details are correct"}




def get_categories():
url = "https://api.shipbubble.com/v1/shipping/labels/categories"
response = make_shipbubble_request(url, method='GET')
return response.get('data', [])




# Helper functions
def handle_authenticated_user_location(profile, form_data):
if profile.delivery_location:
location = profile.delivery_location
if location.formatted_address != form_data['address']:
location.formatted_address = form_data['address']
location.save()
else:
location = Location.objects.create(
formatted_address = form_data['address']
)
profile.delivery_location = location
update_profile(profile, form_data)
print(location)
return location




def handle_authenticated_user_location(profile, form_data):
if profile.delivery_location:
location = profile.delivery_location
if location.formatted_address != form_data['address']:
location.formatted_address = form_data['address']
location.save()
else:
location = Location.objects.create(
formatted_address=form_data['address']
)
profile.delivery_location = location

update_profile(profile, form_data)
profile.save()
return location


def update_profile(profile, form_data):
if profile.phone_number != form_data['phone_number']:
profile.phone_number = form_data['phone_number']
if profile.email != form_data['email']:
profile.email = form_data['email']
profile.save()



def create_order(request, location, form_data, total_amount, payment_reference):

try:
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

except Exception as e:
messages.error(request, f"Error creating order: {str(e)}")
return redirect('cart')

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
response = requests.post(url, headers=headers, json=data)
response.raise_for_status()
return response.json()

except requests.RequestException as e:
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





      "package_amount": "₦1,510,000",
      "package_weight": "2.00KG",
      "pickup_time": "December 19th 2022, 10:57:44 PM"
"""