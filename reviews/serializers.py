# serializers.py
from rest_framework import serializers
from .models import ProductReview
from accounts.serializers import UserSerializer

class ProductReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Use UserSerializer for the 'user' field

    class Meta:
        model = ProductReview
        fields = ['product', 'user', 'comment', 'reply', 'createdat']

    def create(self, validated_data):
        request = self.context.get('request', None)
        validated_data['user'] = request.user

        # Create the ProductReview instance
        instance = ProductReview.objects.create(**validated_data)

        return instance
