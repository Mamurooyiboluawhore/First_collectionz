from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from accounts.models import Wishlist
from accounts.models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WishlistSerializer


class CreateWishlistApi(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            product_ids = request.data.get('product_ids', [])

            if not user_id:
                return Response({'error': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = WishlistSerializer(data={'user_id': user_id, 'product_ids': product_ids})
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Wishlist created successfully",
                    "status_code": 201,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response = {
                "message": "Internal server error",
                "status_code": 500,
                "data": {'detail': str(e)},
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WishlistList(APIView):
    def get(self, request):
        try:
            wishlists = Wishlist.objects.all()
            serializer = WishlistSerializer(wishlists, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WishListdetails(APIView):
    def get_object(self, pk):
        try:
            wishlist = get_object_or_404(Wishlist, pk=pk)
            serializer = WishlistSerializer(wishlist)
            return Response(serializer.data)
        except Wishlist.DoesNotExist:
            return Response({'error': 'Wishlist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            wishlist = get_object_or_404(Wishlist, pk=pk)
            serializer = WishlistSerializer(wishlist, data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Wishlist successfully updated",
                    "status_code": 200,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Wishlist.DoesNotExist:
            return Response({'error': 'Wishlist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            wishlist = get_object_or_404(Wishlist, pk=pk)
            wishlist.delete()
            response = {
                "message": "Wishlist successfully deleted",
                "status_code": 200
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
