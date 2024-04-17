from rest_framework import serializers
from accounts.models import Order, OrderItems, Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'created_at', 'updated_at']

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id', 'product', 'user', 'promo', 'created_at', 'updated_at', 'deleted_at', 'is_delete', 'status']

class OrderItemsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['product', 'user', 'promo', 'status']  # Exclude 'created_at', 'updated_at', 'deleted_at', 'is_delete'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at', 'order_items', 'total_amount']
        read_only_fields = ['id', 'created_at', 'total_amount']  # Ensure id, created_at, and total_amount are read-only

class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemsCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ['customer', 'order_items']  # Exclude 'id', 'created_at', 'total_amount'

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItems.objects.create(order=order, **order_item_data)
        return order
