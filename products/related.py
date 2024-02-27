from accounts.models import Product
from rest_framework.views import APIView


class ProductDetailAPIViews(APIView):
    def get_product(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            products = Product.objects.filter(category=product.category)
            return products
        except Exception as e:
            return get_object_or_404(Product, pk=pk)
        

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



from accounts.models import Product
from accounts.serializers import ProductSerializer  # You need to import the serializer for Product

class ProductDetailAPIViews(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            products_in_category = Product.objects.filter(category=product.category)

            product_serializer = ProductSerializer(product)
            products_in_category_serializer = ProductSerializer(products_in_category, many=True)

            # Return the response with details of the current product and other products in the same category
            response_data = {
                'product': product_serializer.data,
                'other_products_in_category': products_in_category_serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            # Return a 404 response if the product is not found
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

