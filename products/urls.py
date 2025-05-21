from django.urls import path
from .views import ProductListCreateAPIView, ProductDetailAPIView

urlpatterns = [
    # URL for listing all products or retrieving a single product
    path('', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('<uuid:pk>/', ProductListCreateAPIView.as_view(), name='product-detail'),

    # URL pattern for creating, updating, and deleting a specific product
    path('create/', ProductDetailAPIView.as_view(), name='product-create'),
    path('<uuid:pk>/update/', ProductDetailAPIView.as_view(), name='product-update'),
    path('<uuid:pk>/delete/', ProductDetailAPIView.as_view(), name='product-delete'),
]