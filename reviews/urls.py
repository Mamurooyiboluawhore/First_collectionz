from django.urls import path
from .views import ProductReviewDetail, ProductReviewList

urlpatterns = [
    path('product-reviews/', ProductReviewList.as_view(), name='product_review_api'),
    path('product-reviews/<int:review_id>/', ProductReviewDetail.as_view(), name='product_review_detail'),
]
