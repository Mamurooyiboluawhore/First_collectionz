from django.urls import path
from .views import CreateCartApiView, ListApiViews, CartListdetails

urlpatterns = [
    # URL pattern for listing all products and creating new products
    path('', CreateCartApiView.as_view(), name='cart-list-create'),
    path('', ListApiViews.as_view(), name='cart-list'),

    # URL pattern for retrieving, updating, and deleting a specific product
    path('<uuid:pk>/', ListApiViews.as_view(), name='cart-detail'),

    # URL pattern for updating a specific product
    path('<uuid:pk>/update/', CartListdetails.as_view(), name='cart-update'),

    # URL pattern for deleting a specific product
    path('<uuid:pk>/delete/', CartListdetails.as_view(), name='cart-delete'),
]

