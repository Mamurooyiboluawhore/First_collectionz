from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import ProductCategory
from accounts.models import Product
from products.serializers import ProductSerializer
from .serializers import CategorySerializer

# Create your views here.


class CategoryCreateAPIView(APIView):
   def get(self, request):
      try:
         category = ProductCategory.objects.all()
         serializer = CategorySerializer(category, many=True)
         response ={
            "Message": 'List of all category',
            'status_code': 200,
            'data': serializer.data
         }
         return Response(response, status=status.HTTP_200_OK)
      except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
   
   def post(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "category added successfully",
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

class CategoryDetailAPIViews(APIView):
    def get_object(self, pk):
        try:
            return ProductCategory.objects.get(pk=pk)
        except ProductCategory.DoesNotExist:
            return get_object_or_404(ProductCategory, pk=pk)
    
    def get(self, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "category successfully updated",
                "status_code": 200,
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk):
        try:
            product = get_object_or_404(ProductCategory, pk=pk)
            product.delete()
            return Response({'message': 'category deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    

class ProductByCategory(APIView):
    def get(self, request, category_pk, format=None):
        try:
            category = ProductCategory.objects.get(pk=category_pk)
            products = Product.objects.filter(category=category)
            serializer = ProductSerializer(products, many=True)
            response = {
                "message": "products by category successfully retrieved",
                "status_code": 200,
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ProductCategory.DoesNotExist:
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        