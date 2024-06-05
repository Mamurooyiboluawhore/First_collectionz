from rest_framework import serializers
from accounts.models import Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'quantity', 'category', 'user', 'price', 'discount_price', 'admin_status', 'image', 'size', 'colours']
        
        
