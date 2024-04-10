from django.urls import path
from .views import ProductListCreateAPIView, ProductDetailAPIViews

urlpatterns = [
    # URL pattern for listing all products and creating new products
    path('', ProductListCreateAPIView.as_view(), name='product-list-create'),

    # URL pattern for retrieving, updating, and deleting a specific product
    path('<uuid:pk>/', ProductDetailAPIViews.as_view(), name='product-detail'),

    # URL pattern for updating a specific product
    path('<uuid:pk>/update/', ProductDetailAPIViews.as_view(), name='product-update'),

    # URL pattern for deleting a specific product
    path('<uuid:pk>/delete/', ProductDetailAPIViews.as_view(), name='product-delete'),
]

