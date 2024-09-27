from django.contrib import admin
from .models import Category, Product, Order, OrderItem, CartItem, Cart, FAQ, SearchedProduct
from .models import PaymentSettings



@admin.register(PaymentSettings)
class PaymentSettingsAdmin(admin.ModelAdmin):
    list_display = ['tax_rate', 'shipping_rate', 'discount_rate']



@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_visible')
    list_editable = ('order', 'is_visible')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'url']
    prepopulated_fields = {'slug': ('name',)}
    #fields = ['name', 'slug', 'url']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'section', 'available', 'created_at', 'updated_at']

    list_display = ['name', 'slug', 'price', 'stock', 'section', 'available', 'created_at', 'updated_at']
    list_filter = ['available', 'category', 'section', 'created_at', 'updated_at']
    list_editable = ['price', 'stock', 'available', 'section']
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    filter_horizontal = ('category',)

class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    inlines = [CartItemInline]



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_name', 'get_phone_number', 'get_total_amount', 'paid', 'status', 'created_at']
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
        if obj:  
            return self.readonly_fields #+ ('total_amount')
        return self.readonly_fields

    def has_delete_permission(self, request, obj=None):
        return False  

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'quantity', 'price']
    list_filter = ['order__status']
    raw_id_fields = ['order', 'product']
    search_fields = ['order__name', 'product__name']

    def has_add_permission(self, request):
        return False  

    def has_delete_permission(self, request, obj=None):
        return False  


@admin.register(SearchedProduct)
class SearchedProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'searched_at']
    list_filter = ['searched_at']
    search_fields = ['name']
    readonly_fields = ['searched_at']
    ordering = ['-searched_at']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

"""
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    search_fields = ['email']
"""
# Customize the admin site header and title
admin.site.site_header = 'JollyLife Health E-commerce Admin'
admin.site.site_title = 'JollyLife Health E-commerce Admin Portal'
admin.site.index_title = 'Welcome to JollyLife Health E-commerce Portal'