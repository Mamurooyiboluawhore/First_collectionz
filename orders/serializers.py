from rest_framework import serializers
from accounts.models import Order


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        models = Order
        fields = '__all__'