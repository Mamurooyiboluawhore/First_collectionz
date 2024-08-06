from products.models import Product
from products.serializers import ProductSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class Recommendation(APIView):
    """
    API endpoint for recommending similar products based on a given product.

       - Allows users to get recommendations for products similar to the specified product.

    Handles GET requests for recommending similar products.

       Args:
           request: The HTTP request object.
           product_id: The ID of the product for which similar products are recommended.

       Returns:
           Response: JSON response containing a list of recommended similar products.

    """
    def get(self, request, product_id):
        try:
            current_product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({}, "Product not found")

        try:
            similar_products = Product.objects.filter(
                category=current_product.category,
                is_deleted='active',
                admin_status='approved',
            ).exclude(id=product_id)

            recommended_products = similar_products[:4]

            serializer = ProductSerializer(recommended_products, many=True)

            data = {
                "similar_products": serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            data = {
                "error_message": f"An error occurred while while retrieving products you might like: {str(e)}",
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
