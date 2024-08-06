from rest_framework import serializers
from products.models import Product


class SortSerializer(serializers.ModelSerializer):
    class Meta():
        model = Product
        field = '__all__'