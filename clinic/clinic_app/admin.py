from django.contrib import admin
from .models import Category, Product, Order, OrderItem, CartItem, Cart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'category', 'section', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'category', 'section', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available', 'category', 'section']
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'created_at', 'updated_at']
    inlines = [CartItemInline]



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_name', 'get_phone_number', 'get_total_amount', 'paid', 'status', 'created_at']
    list_filter = ['paid', 'status', 'created_at']
    search_fields = ['name', 'phone_number', 'delivery_location']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at']
    fieldsets = (
        (None, {
            'fields': ('created_at',)
        }),
        ('Customer Information', {
            'fields': ('name', 'phone_number', 'delivery_location', 'order_note')
        }),
        ('Order Details', {
            'fields': ('total_amount', 'paid', 'status')
        }),
    )

    def get_name(self, obj):
        return obj.name
    get_name.short_description = 'Name'

    def get_phone_number(self, obj):
        return obj.phone_number
    get_phone_number.short_description = 'Phone Number'

    def get_total_amount(self, obj):
        return obj.total_amount
    get_total_amount.short_description = 'Total Amount'

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields #+ ('total_amount')
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion of orders

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_filter = ['order__status']
    raw_id_fields = ['order', 'product']
    search_fields = ['order__name', 'product__name']

    def has_add_permission(self, request):
        return False  # Prevent adding order items directly

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion of order items
"""
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    search_fields = ['email']
"""
# If you want to customize the admin site header and title
admin.site.site_header = 'Jolly Life Health E-commerce Admin'
admin.site.site_title = 'Jolly Life Health E-commerce Admin Portal'
admin.site.index_title = 'Welcome to Jolly Life Health E-commerce Portal'