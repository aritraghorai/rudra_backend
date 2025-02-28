from rest_framework import serializers

from products.serializers import ProductDesignSerializer, ProductVariantGetSerializer

from .models import Cart, CartItem, Order, OrderItem

class CartItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    variant = ProductVariantGetSerializer()
    design = ProductDesignSerializer()
    class Meta:
        model = CartItem
        fields = ['id', 'variant', 'design', 'quantity', 'total_price']
    
    def get_total_price(self, obj):
        return obj.get_total_price()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_amount']
    
    def get_total_amount(self, obj):
        return obj.get_total_amount()

class OrderItemSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['variant', 'design', 'quantity', 'variant_price', 'design_price', 'total_price']
    
    def get_total_price(self, obj):
        return obj.get_total_price()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'status', 'total_amount', 'shipping_address', 
                 'contact_number', 'items']
