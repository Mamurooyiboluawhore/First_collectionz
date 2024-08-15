from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Product
from .serializers import ProductSerializer

class ProductListCreateAPIView(APIView):
    """
    API endpoint for listing products or retrieving a single product.

    GET:
    - If `pk` is provided, retrieves a single product by ID.
    - If `pk` is not provided, returns a list of all products.

    Raises:
    - HTTP_500_INTERNAL_SERVER_ERROR: If an internal server error occurs.
    """
    def get(self, request, pk=None, format=None):
        """
        Handles GET requests for retrieving product(s).
        
        Args:
        - request: HTTP request object.
        - pk: The primary key of the product (optional).
        - format: The requested data format (optional).

        Returns:
        - Response containing product data or an error message.
        """
        try:
            if pk:
                product = get_object_or_404(Product, pk=pk)
                serializer = ProductSerializer(product)
                return Response({
                    'msg': "Product item",
                    'status_code': status.HTTP_200_OK,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                products = Product.objects.all()
                serializer = ProductSerializer(products, many=True)
                return Response({
                    'msg': "Product list",
                    'status_code': status.HTTP_200_OK,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetailAPIView(APIView):
    """
    API endpoint for creating, updating, and deleting individual products.

    POST:
    - Creates a new product.

    PUT:
    - Updates details of a specific product.

    DELETE:
    - Deletes a specific product.

    Raises:
    - HTTP_404_NOT_FOUND: If the requested product does not exist.
    - HTTP_500_INTERNAL_SERVER_ERROR: If an internal server error occurs.
    """
    permission_classes = [IsAdminUser]

    def post(self, request, format=None):
        """
        Creates a new product.

        Args:
        - request: HTTP request object.
        - format: The requested data format. Default is None.

        Returns:
        - Response containing information about the created product or validation errors.
        """
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Product added successfully",
                    "status_code": status.HTTP_201_CREATED,
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": "Internal server error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": {'detail': str(e)},
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk, format=None):
        """
        Updates details of a specific product.

        Args:
        - request: HTTP request object.
        - pk: The primary key of the product.
        - format: The requested data format. Default is None.

        Returns:
        - Response containing updated details of the product or validation errors.
        """
        try:
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Product successfully updated",
                    "status_code": status.HTTP_200_OK,
                    "data": serializer.data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                "message": "Internal server error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": {'detail': str(e)},
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk, format=None):
        """
        Deletes a specific product.

        Args:
        - request: HTTP request object.
        - pk: The primary key of the product.

        Returns:
        - Response confirming the deletion of the product.
        """
        try:
            product = get_object_or_404(Product, pk=pk)
            product.delete()
            return Response({
                'message': 'Product deleted successfully.',
                'status_code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "message": "Internal server error",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": {'detail': str(e)},
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
