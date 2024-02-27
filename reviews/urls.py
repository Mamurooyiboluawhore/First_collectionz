from django.urls import path
from .views import ProductReviewDetail, ProductReviewList

urlpatterns = [
    path('list/', ProductReviewList.as_view(), name='product-review-api'),
    path('', ProductReviewDetail.as_view(), name='create-product-reviews'),
    path('<int:review_id>/details/', ProductReviewDetail.as_view(), name='product_review_detail'),
    path('<int:review_id>/delete', ProductReviewDetail.as_view(), name='product_review_delete'),
]
