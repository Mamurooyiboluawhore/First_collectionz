from rest_framework import serializers
from accounts.models import Cart, Product
from products.serializers import ProductSerializer 


class CartSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta():
        model = Cart
        field = '__all__'