# from django.http import JsonResponse
# from django.shortcuts import render
# from django.shortcuts import get_object_or_404
# from accounts.models import Cart
# from accounts.models import Product
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import CartSerializer
# from rest_framework.permissions import IsAuthenticated


# class CreateCartApiView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         try:
#             product_id = request.data.get('product_id')
#             if not product_id:
#                 return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

#             try:
#                 product = Product.objects.get(pk=product_id)
#             except Product.DoesNotExist:
#                 return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

#             data = request.data.copy()
#             data['product'] = product.id
#             data['user'] = request.user.id

#             serializer = CartSerializer(data=data)
#             if serializer.is_valid():
#                 serializer.save()
#                 response = {
#                     "message": "Product successfully added to cart",
#                     "status_code": 201,
#                     "data": serializer.data
#                 }
#                 return Response(response, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             response = {
#                 "message": "Internal server error",
#                 "status_code": 500,
#                 "data": {'detail': str(e)},
#             }
#             return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class ListApiViews(APIView):
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, pk=None):
#         try:
#             if pk:
#                 cart = get_object_or_404(Cart, pk=pk, user=request.user)
#                 serializer = CartSerializer(cart)
#                 response = {
#                     'message': 'Cart item',
#                     'status_code': 200,
#                     'data': serializer.data
#                 }
#             else:
#                 carts = Cart.objects.filter(user=request.user)
#                 serializer = CartSerializer(carts, many=True)
#                 response = {
#                     "message": "List of cart",
#                     "status_code": 200,
#                     "data": serializer.data                 
#                 }
#             return Response(response, status=status.HTTP_200_OK)
#         except Exception as e:
#             res = {
#                 'message': "Internal server error",
#                 'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 "error": str(e) 
#             }
#             return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
  
# class CartListdetails(APIView):
#     permission_classes = [IsAuthenticated]

#     def put(self, pk, request):
#         try:
#             cart = get_object_or_404(Cart, pk=pk, user=request.user)
#             serializer = CartSerializer(cart)
#             if serializer.is_valid():
#                 serializer.save
#                 response = {
#                     "message": "cart successfully updated",
#                     "staus_code": 200,
#                     "data":serializer.data
#                 }
#                 return Response(response, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#     def delete(self, pk, request):
#         try:
#             cart = get_object_or_404(Cart, pk=pk,  user=request.user)
#             cart.delete()
#             response = {
#                 "message": "Cart successfully deleted",
#                 "status_code": 204,
#             }
#             return Response(response, status=status.HTTP_204_NO_CONTENT)
        
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




from django.shortcuts import get_object_or_404
from accounts.models import Product
from .models import Cart
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated

class CreateCartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.data.get('product_id')
            if not product_id:
                return Response({'detail': 'Product ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(pk=product_id)
            except Product.DoesNotExist:
                return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

            data = request.data.copy()
            data['product'] = product.id
            data['user'] = request.user.id

            serializer = CartSerializer(data=data)
            if serializer.is_valid():
                cart_instance = serializer.save()
                response = {
                    "message": "Product successfully added to cart",
                    "status_code": 201,
                    "cart_id": cart_instance.id, 
                    "data": serializer.data
                }
                
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "message": "Internal server error",
                "status_code": 500,
                "data": {'detail': str(e)},
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListApiViews(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        try:
            if pk:
                cart = get_object_or_404(Cart, pk=pk, user=request.user)
                serializer = CartSerializer(cart)
                response = {
                    'message': 'Cart item',
                    'status_code': 200,
                    'data': serializer.data
                }
            else:
                carts = Cart.objects.filter(user=request.user)
                serializer = CartSerializer(carts, many=True)
                response = {
                    "message": "List of cart items",
                    "status_code": 200,
                    "data": serializer.data
                }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            res = {
                'message': "Internal server error",
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                "error": str(e)
            }
            return Response(res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CartListDetails(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            cart = get_object_or_404(Cart, pk=pk, user=request.user)
            serializer = CartSerializer(cart, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Cart successfully updated",
                    "status_code": 200,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            cart = get_object_or_404(Cart, pk=pk, user=request.user)
            cart.delete()
            response = {
                "message": "Cart successfully deleted",
                "status_code": status.HTTP_204_NO_CONTENT
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ProductCart(APIView):
    def get(self, request, product_id):
        try:
            cart_exists = Cart.objects.filter(product_id=product_id, user=request.user).exists()
            if cart_exists:
                response = {
                    'message': True,
                    'status': status.HTTP_200_OK
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'message': False,
                    'status': status.HTTP_200_OK
                    }
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


