from rest_framework import serializers
from accounts.models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        field = '__all__'