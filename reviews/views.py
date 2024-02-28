from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import ProductReview
from .serializers import ProductReviewSerializer


class ProductReviewList(APIView):
    """
    API endpoint for retrieving a list of product reviews.

        - Allows users to get a list of reviews for products.

    Handles GET requests for retrieving product reviews.

        Args:
            request: The HTTP request object.

        Returns:
            Response: JSON response containing a list of product reviews.
    """
    def get(self, request):
        try:
            product_reviews = ProductReview.objects.all()
            serializer = ProductReviewSerializer(product_reviews, many=True)
            data = {
                "product_reviews": serializer.data,
                "message": "List of Product Reviews",
            }
            return Response(data, status.HTTP_200_OK)

        except Exception as e:
            data = {
                "error_message": f"An error occurred while retrieving product reviews: {str(e)}",
            }
            return Response(data, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductReviewDetail(APIView):
    """
    API endpoint for managing individual product reviews.

    - Allows users to retrieve, add, update, or delete product reviews.
    """

    def post(self, request):
        """
        Add a new product review.

        - Allows users to add a new review for a product.
        """
        data = request.data
        data['user'] = request.user

        serializer = ProductReviewSerializer(data=data,  context={'request': request})
        try:
            if serializer.is_valid():
                serializer.save()
                data = {
                    "product_review": serializer.data
                }
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {
                "error_message": f"An error occurred while adding a product review: {str(e)}",
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self, review_id):
        """
        Retrieve a specific product review.

        - Allows users to retrieve details of a specific product review.
        """
        return get_object_or_404(ProductReview, id=review_id)

    def get(self, request, review_id):
        """
        Retrieve a product review.

        - Allows users to retrieve details of a specific product review.
        """
        review = self.get_object(review_id)
        serializer = ProductReviewSerializer(review)
        return Response(serializer.data)

    def delete(self, request, review_id):
        """
        Remove a product review.

        - Allows users to remove a product review.
        """
        try:
            review = self.get_object(review_id)
            review.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            data = {
                "error_message": f"An error occurred while removing a product review: {str(e)}",
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, review_id):
        """
        Update a product review.

        - Allows users to update a product review.
        """
        review = self.get_object(review_id)
        data = request.data
        serializer = ProductReviewSerializer(review, data=data)

        try:
            if serializer.is_valid():
                serializer.save()
                data = {
                    "product_review": serializer.data
                }
                return Response(data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            data = {
                "error_message": f"An error occurred while updating a product review: {str(e)}",
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
