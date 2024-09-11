"""
# api/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'name', 'phone_number', 'delivery_location', 'order_note', 
                  'total_amount', 'status', 'created_at', 'items']
"""

from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ['id', 'session_key', 'delivery_location', 'name', 'phone_number', 
                  'order_note', 'total_amount', 'payment_reference', 'created_at', 
                  'paid', 'status', 'items']
        read_only_fields = ['id', 'session_key', 'delivery_location', 'name', 'phone_number', 
                            'order_note', 'total_amount', 'payment_reference', 'created_at', 
                            'paid', 'items']