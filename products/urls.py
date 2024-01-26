from django.urls import path
from .views import (
    ProductListCreateAPIView,
    ProductDetailAPIViews,
)

urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('<uuid:pk>/', ProductDetailAPIViews.as_view(), name='product-detail'),
    path('<uuid:pk>/details/', ProductDetailAPIViews.as_view(), name='product-details'),
    path('<uuid:pk>/delete/', ProductDetailAPIViews.as_view(), name='product-delete'),
]
