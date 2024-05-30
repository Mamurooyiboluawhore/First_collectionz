from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from accounts.models import Cart
from accounts.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated


class CreateCartApiView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            serializer = CartSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Product successfully added to cart",
                    "status_code": 200,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # except Exception as e:
        #     response = {
        #         "message": "internal server error",
        #         "status_code": 500,
        #         "data": serializer.data
        #     }
        #     return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            response= {
                "message": "internal server error",
                "status_code": 500,
                "data": {'detail': str(e)},
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListApiViews(APIView):
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk, requst):
        try:
            cart = get_object_or_404(Cart, pk=pk)
            serializer = CartSerializer(cart)
            response = {
                "messasge": "list of cart",
                "status_code": 200,
                "data": serializer.data                 
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("internal server error", status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


    def get(self, request):
        try:
            cart = Cart.objects.all()
            serializer = CartSerializer(cart, many=True)
            response = {
                "message": "List of all cart",
                "status_code": 200,
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class CartListdetails(APIView):
    # permission_classes = [IsAuthenticated]

    def put(self, pk, request):
        try:
            cart = Cart.objects.get(pk=pk)
            serializer = CartSerializer(cart)
            if serializer.is_valid():
                serializer.save
                response = {
                    "message": "cart successfully updated",
                    "staus_code": 200,
                    "data":serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def delete(self, pk, request):
        try:
            cart = get_object_or_404(Cart, pk=pk)
            cart.delete()
            response = {
                "message": "Cart successfully deleted",
                "status_code": 204,
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        