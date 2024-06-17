# from django.http import JsonResponse
# from django.shortcuts import get_object_or_404
# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from accounts.models import Product
# from .serializers import ProductSerializer
# from rest_framework.permissions import IsAuthenticated, IsAdminUser

# class ProductListCreateAPIView(APIView):
#     """
#     API endpoint for listing and creating products.

#     GET:
#     Returns a list of all products.

#     POST:
#     Creates a new product.

#     Raises:
#     HTTP_500_INTERNAL_SERVER_ERROR: If an internal server error occurs.
#     """
#     def get(self, request, format=None):
#         """
#         Retrieves a list of all products.

#         Args:
#         request: HTTP request object.
#         format: The requested data format. Default is None.

#         Returns:
#         Response containing a list of serialized products.
#         """
#         try:
#             products = Product.objects.all()
#             serializer = ProductSerializer(products, many=True)
#             return Response(serializer.data)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request, format=None):
#         """
#         Creates a new product.

#         Args:
#         request: HTTP request object.
#         format: The requested data format. Default is None.

#         Returns:
#         Response containing information about the created product or validation errors.
#         """
#         # self.permission_classes = [IsAuthenticated, IsAdminUser] 
#         try:
#             serializer = ProductSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 response = {
#                     "message": "Product added successfully",
#                     "status_code": 201,
#                     "data" : serializer.data
#                 }
#                 return Response(response, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             response= {
#                 "message": "internal server error",
#                 "status_code": 500,
#                 "data": {'detail': str(e)},
#             }
#             return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ProductDetailAPIViews(APIView):
#     """
#     API endpoint for retrieving, updating, and deleting individual products.

#     GET:
#     Retrieves details of a specific product.

#     PUT:
#     Updates details of a specific product.

#     DELETE:
#     Deletes a specific product.

#     Raises:
#     HTTP_404_NOT_FOUND: If the requested product does not exist.
#     HTTP_500_INTERNAL_SERVER_ERROR: If an internal server error occurs.
#     """
#     def get_object(self, pk):
#         """
#         Helper function to retrieve a product object by its primary key (pk).

#         Args:
#         pk: The primary key of the product.

#         Returns:
#         Product object.

#         Raises:
#         HTTP_404_NOT_FOUND: If the product with the given primary key does not exist.
#         """
#         try:
#             return Product.objects.get(pk=pk)
#         except Product.DoesNotExist:
#             return get_object_or_404(Product, pk=pk)
    
    
#     def get(self, request, pk, format=None):
#         """
#         Retrieves details of a specific product.

#         Args:
#         request: HTTP request object.
#         pk: The primary key of the product.
#         format: The requested data format. Default is None.

#         Returns:
#         Response containing details of the specified product.
#         """
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         """
#         Updates details of a specific product.

#         Args:
#         request: HTTP request object.
#         pk: The primary key of the product.
#         format: The requested data format. Default is None.

#         Returns:
#         Response containing updated details of the product or validation errors.
#         """
#         # self.permission_classes = [IsAuthenticated, IsAdminUser]
#         product = self.get_object(pk)
#         serializer = ProductSerializer(product, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             response = {
#                 "message": "Product successfully updated",
#                 "status_code": 200,
#                 "data": serializer.data
#             }
#             return Response(response, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#     def delete(self, request, pk):
#         """
#         Deletes a specific product.

#         Args:
#         request: HTTP request object.
#         pk: The primary key of the product.

#         Returns:
#         Response confirming the deletion of the product.
#         """
#         # self.permission_classes = [IsAuthenticated, IsAdminUser]
#         try:
#             product = get_object_or_404(Product, pk=pk)
#             product.delete()
#             return Response({'message': 'Product deleted successfully.'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)