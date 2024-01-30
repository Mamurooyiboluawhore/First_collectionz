from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import ProductCategory
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
         return Response(response, status=status.HTTP_200_SUCCESS)
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
    
    def get(self, request, pk, format=None):
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
            return JsonResponse({'message': 'catw deleted successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)