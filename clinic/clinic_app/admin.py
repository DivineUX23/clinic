from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Cart, CartItem, Newsletter
"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
"""
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'category', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'category', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available', 'category',]
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at', 'paid', 'status']
    list_filter = ['paid', 'created_at', 'updated_at', 'status']
    inlines = [OrderItemInline]

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    inlines = [CartItemInline]

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    search_fields = ['email']

# If you want to customize the admin site header and title
admin.site.site_header = 'Jolly Life Health E-commerce Admin'
admin.site.site_title = 'Jolly Life Health E-commerce Admin Portal'
admin.site.index_title = 'Welcome to Jolly Life Health E-commerce Portal'