# from rest_framework import serializers
# from accounts.models import Cart, Product
# from products.serializers import ProductSerializer 


# class CartSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=True, read_only=True)
#     class Meta():
#         model = Cart
#         fields = '__all__'

#         extra fields = ['product', 'user', 'createdat' 'updatedat']



# class CartSerializer(serializers.ModelSerializer):
#     product_details = serializers.SerializerMethodField()

#     class Meta:
#         model = Cart
#         fields = ['id', 'user', 'product', 'product_details']

#     def get_product_details(self, obj):
#         if obj.product:
#             return ProductSerializer(obj.product).data
#         return None
    
    

from rest_framework import serializers
from accounts.models import Cart, Product

class CartSerializer(serializers.ModelSerializer):
    product_details = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'user', 'product_details']
        extra_kwargs = {
            'product': {'write_only': True},
        }

    def get_product_details(self, obj):
        product = obj.product
        if product:
            return {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'quantity': product.quantity,
                'price': product.price,
                'discount_price': product.discount_price,
                'admin_status': product.admin_status,
                'is_deleted': product.is_deleted,
                'is_published': product.is_published,
                'currency': product.currency,
                'image': product.image.url if product.image else None,
                'size': product.size,
                'colours': product.colours,
                'category': product.category_id,
                'rating': product.rating_id,
                'sub_category': product.sub_category_id
            }
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_details = representation.pop('product_details')
        cart_id = representation.pop('id')
        if product_details:
            representation.update(product_details)
        representation['cart_id'] = cart_id
        return representation
