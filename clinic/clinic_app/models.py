from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.urls import reverse
from decimal import Decimal
from ckeditor.fields import RichTextField



from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    delivery_location = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.user.username

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
    """
    CATEGORY_CHOICES = [
        ('new_arrival', 'New Arrival'),
        ('most_popular', 'Most Popular'),
    ]
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    #description = models.TextField()
    description = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], db_index=True)
    #category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    category = models.ManyToManyField(Category, related_name='products', db_index=True)
    #section = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    url = models.URLField(max_length=500, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)


    view_count = models.PositiveIntegerField(default=0, db_index=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])


    def increment_view_count(self):
        self.view_count += 1
        self.save()



class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    session_key = models.CharField(max_length=40, null=True, blank=True)
    delivery_location = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    order_note = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_reference = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
        
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} by {self.name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

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
