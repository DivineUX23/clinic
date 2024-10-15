from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from decimal import Decimal
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from cities_light.models import Country, Region, City






class Location(models.Model):
    street_no = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    formatted_address = models.CharField(max_length=255, blank=True)

    #latitude = models.FloatField(null=True, blank=True)
    #longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.formatted_address
    """
    def get_formatted_address(self):
        components = []
        if self.street_no:
            components.append(self.street_no)
        if self.street:
            components.append(self.street)
        if self.city:
            components.append(self.city.name)
        if self.state:
            components.append(self.state.name)
        if self.postal_code:
            components.append(self.postal_code)
        if self.country:
            components.append(self.country.name)
        
        return ", ".join(filter(None, components))

    def save(self, *args, **kwargs):
        self.formatted_address = self.get_formatted_address()
        super().save(*args, **kwargs)
    """



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    #delivery_location = models.CharField(max_length=255, blank=True, null=True)
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
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    delivery_location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=150)
    order_note = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    service_code = models.CharField(max_length=100, null=True, blank=True)  # Made nullable
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Made nullable
    tracking_number = models.CharField(max_length=100, null=True, blank=True)  # Changed to CharField
        
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    courier_id = models.CharField(max_length=255, null=True, unique=False)
    request_token = models.CharField(max_length=255, null=True, unique=False)

    order_category = models.CharField(max_length=255, null=True, unique=False)


    # New fields for shipment information
    shipment_order_id = models.CharField(max_length=50, blank=True, null=True)
    courier_name = models.CharField(max_length=100, blank=True, null=True)
    courier_email = models.EmailField(blank=True, null=True)
    courier_phone = models.CharField(max_length=20, blank=True, null=True)
    shipment_status = models.CharField(max_length=20, blank=True, null=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    package_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    tracking_url = models.URLField(blank=True, null=True)
    shipment_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_formatted_delivery_address(self):
        if self.delivery_location:
            return self.delivery_location.formatted_address
        return "No delivery address set"

    def get_total_with_shipping(self):
        return self.total_amount + (self.shipping_cost or Decimal('0.00'))



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




class SenderAddress(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sender_address')
    email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    street_no = models.CharField(max_length=10)
    street = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    formatted_address = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name_plural = "Sender Addresses"

    def __str__(self):
        return self.formatted_address

    def get_formatted_address(self):
        components = []
        if self.street_no:
            components.append(self.street_no)
        if self.street:
            components.append(self.street)
        if self.city:
            components.append(self.city)
        if self.state:
            components.append(self.state)
        if self.postal_code:
            components.append(self.postal_code)
        if self.country:
            components.append(self.country)
        
        return ", ".join(filter(None, components))

    def save(self, *args, **kwargs):
        self.formatted_address = self.get_formatted_address()
        super().save(*args, **kwargs)




