from rest_framework import serializers
from accounts.models import Order


class OrderSerializers(serializers.ModelSerializers):
    class Meta:
        models = Order
        fields = '__all__'