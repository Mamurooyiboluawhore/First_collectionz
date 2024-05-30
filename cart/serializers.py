from rest_framework import serializers
from accounts.models import Cart, Product
from products.serializers import ProductSerializer 


# class CartSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True, read_only=True)
#     class Meta():
#         model = Cart
#         fields = '__all__'

#         extra fields = ['product', 'user', 'createdat' 'updatedat']



class CartSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'product_details', 'created_at', 'updated_at']

    def get_product_details(self, obj):
        if obj.product:
            return ProductSerializer(obj.product).data
        return None