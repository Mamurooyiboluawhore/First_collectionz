from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(APIView):
    def get(self, request, format=None):
        try:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Product added successfully",
                    "status_code": 201,
                    "data" : serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response= {
                "message": "internal server error",
                "status_code": 500,
                "data": {'detail': str(e)},
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetailAPIViews(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return get_object_or_404(Product, pk=pk)
    
    
    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Product successfully updated",
                "status_code": 200,
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        try:
            product = get_object_or_404(Product, pk=pk)
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)