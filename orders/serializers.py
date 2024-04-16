from rest_framework import serializers
from accounts.models import Order


class OrderSerializers(serializers.ModelSerializer):

    class Meta:
        models = Order
        fields = ['id', 'customer', 'order_date', 'order_items', 'total_amount' ]






class CreateOrderSeriaizers(serializers.Serializer):
    cart_id = serializers.UUIDfield()

    def save(self, **kwargs):
        return super().save(**kwargs)
    
