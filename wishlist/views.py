from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from accounts.models import Wishlist
from accounts.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WishlistSerializer
# Create your views here.

class WishlistApi(APIView):
    def post(self, request):
        try:
            serializer = WishlistSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product_id = serializer.validated_data.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            wishlist, created = Wishlist.objects.get_or_create(user=request.user)
            wishlist.products.add(product)
            context = {
                'message': 'Product added to wishlist',
                'status_code': 201,
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist as e:
            return Response({'error': 'Product does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
