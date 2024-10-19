from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from decimal import Decimal
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from cities_light.models import Country, Region, City
from django.conf import settings
import logging

logger = logging.getLogger(__name__)







class Location(models.Model):
    formatted_address = models.CharField(max_length=255, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.formatted_address
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    #email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    #first_name = models.CharField(max_length=100)
    #last_name = models.CharField(max_length=100)
    delivery_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_delivery_address(self):
        if self.delivery_location:
            return self.delivery_location.formatted_address
        return "No delivery address set"


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()






class PaymentSettings(models.Model):
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.05'))
    shipping_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1000.00'))
    discount_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return "Payment Settings"



class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order']


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    url = models.URLField(max_length=500, blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name



class Product(models.Model):
    
    CATEGORY_CHOICES = [
        ('new_arrival', 'New Arrival'),
        ('most_popular', 'Most Popular'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], db_index=True)
    category = models.ManyToManyField(Category, related_name='products', db_index=True)
    section = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    url = models.URLField(max_length=500, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)


    add_to_cart_count = models.PositiveIntegerField(default=0, db_index=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])


    def increment_add_count(self):
        self.add_to_cart_count += 1
        self.save()



class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    delivery_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    order_note = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    order_category = models.CharField(max_length=255, null=True, unique=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.user.get_full_name()}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())




class ShippingInfo(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_info')

    shipment_id = models.CharField(max_length=50, blank=True, null=True)
    service_code = models.CharField(max_length=100, null=True, blank=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    courier_id = models.CharField(max_length=255, null=True)
    courier_name = models.CharField(max_length=100, blank=True, null=True)
    courier_email = models.EmailField(blank=True, null=True)
    courier_phone = models.CharField(max_length=20, blank=True, null=True)
    shipment_status = models.CharField(max_length=20, blank=True, null=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tracking_url = models.URLField(blank=True, null=True)
    shipment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Shipping Info for Order {self.order.id}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity
    


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, unique=True, null=True, blank=True)
    def __str__(self):
        return f"Cart {self.id}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price

    

class SearchedProduct(models.Model):
    name = models.CharField(max_length=200)
    searched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


"""
import requests
class SenderAddress(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sender_address')
    email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    
    formatted_address = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Sender Addresses"

    def save(self, *args, **kwargs):
        validation_result = self.get_delivery_address()
        if validation_result.get('status') == 'error':
            #raise ValueError(validation_result.get('message', 'Error validating address.'))
            return {'status': 'error', 'message': 'No address provided'}
        super(SenderAddress, self).save(*args, **kwargs)
    
    def get_delivery_address(self):
        print(self.address)
        if not self.address:
            return {'status': 'error', 'message': 'No address provided'}

        url = "https://api.shipbubble.com/v1/shipping/address/validate"
        data = {
            "phone": self.phone_number,
            "email": self.email,
            "name": f"{self.admin.first_name} {self.admin.last_name}",
            "address": self.address
        }

        headers = {
            "Authorization": f"Bearer {settings.SHIPBUBBLE_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()

            if response_data.get('status') == 'success' and 'data' in response_data:
                address_data = response_data['data']
                if 'address_code' in address_data:
                    self.formatted_address = address_data.get('formatted_address', '')
                    self.latitude = address_data.get('latitude')
                    self.longitude = address_data.get('longitude')
                    self.save()  # Save the instance with updated fields
                    return {'status': 'success', 'address': self.formatted_address}
                else:
                    logger.warning(f"Unexpected success response structure: {response_data}")
                    return {'status': 'error', 'message': 'Unexpected response structure'}

            elif response_data.get('status') == 'error':
                error_message = "Error validating address. Please contact support."
                if '422' in response_data.get("message", ""):
                    error_message = "Error validating sender's details. Please contact support."
                elif '400' in response_data.get("message", ""):
                    error_message = "Error validating sender's address. Please contact support."

                self.formatted_address = error_message
                self.save()
                logger.error(f"ShipBubble API error: {response_data}")
                return {'status': 'error', 'message': error_message}

            else:
                logger.error(f"Unexpected response from ShipBubble API: {response_data}")
                return {'status': 'error', 'message': "Unexpected error. Please try again later."}

        except requests.RequestException as e:
            logger.error(f"Request to ShipBubble API failed: {str(e)}")
            return {'status': 'error', 'message': "Could not connect to validation service. Please try again later."}
"""



















from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

class SenderAddress(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_addresses', limit_choices_to={'is_staff': True})
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    
    formatted_address = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    validation_error = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Sender Addresses"

    def save(self, *args, **kwargs):
        validation_result = self.get_delivery_address()
        if validation_result.get('status') == 'error':
            self.validation_error = validation_result.get('message', 'Error validating address.')
        else:
            self.validation_error = None
        super(SenderAddress, self).save(*args, **kwargs)
    
    def get_delivery_address(self):
        if not self.address:
            return {'status': 'error', 'message': 'No address provided'}

        url = "https://api.shipbubble.com/v1/shipping/address/validate"
        data = {
            "phone": self.phone_number,
            "email": self.admin.email,
            "name": f"{self.admin.first_name} {self.admin.last_name}",
            "address": self.address
        }

        headers = {
            "Authorization": f"Bearer {settings.SHIPBUBBLE_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            print(data)
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            print(f"..................{response_data}")

            if response_data.get('status') == 'success' and 'data' in response_data:
                address_data = response_data['data']
                if 'address_code' in address_data:
                    self.formatted_address = address_data.get('formatted_address', '')
                    self.latitude = address_data.get('latitude')
                    self.longitude = address_data.get('longitude')
                    return {'status': 'success', 'address': self.formatted_address}
                else:
                    logger.warning(f"Unexpected success response structure: {response_data}")
                    return {'status': 'error', 'message': 'Unexpected response structure'}

            elif response_data.get('status') == 'error':
                error_message = "Error validating address. Please contact support."
                if '422' in response_data.get("message", ""):
                    error_message = "Error validating sender's details. Please contact support."
                elif '400' in response_data.get("message", ""):
                    error_message = "Error validating sender's address. Please contact support."

                logger.error(f"ShipBubble API error: {response_data}")
                return {'status': 'error', 'message': error_message}

            else:
                logger.error(f"Unexpected response from ShipBubble API: {response_data}")
                return {'status': 'error', 'message': "Unexpected error. Please try again later."}

        except requests.RequestException as e:
            logger.error(f"Request to ShipBubble API failed: {str(e)}")
            return {'status': 'error', 'message': "Could not connect to validation service. Please try again later."}