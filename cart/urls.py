from django.urls import path
from .views import CreateCartApiView, ListApiViews, CartListDetails, ProductCart

urlpatterns = [
    # URL pattern for listing all products and creating new products
    path('create/', CreateCartApiView.as_view(), name='cart-list-create'),
    path('', ListApiViews.as_view(), name='cart-list'),

    # URL pattern for retrieving, updating, and deleting a specific product
    path('<uuid:pk>/', ListApiViews.as_view(), name='cart-item'),

    # URL pattern for updating a specific product
    path('<uuid:pk>/update/', CartListDetails.as_view(), name='cart-update'),

    # URL pattern for deleting a specific product
    path('<uuid:pk>/delete/', CartListDetails.as_view(), name='cart-delete'),
    path('cart/product-in-cart/<int:product_id>/', ProductCart.as_view(), name='product_in_cart'),
]

