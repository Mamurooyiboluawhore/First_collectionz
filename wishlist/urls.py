from django.urls import path
from .views import CreateWishlistApi, WishListdetails, WishlistList


urlpatterns = [
    path('create-wishlist/', CreateWishlistApi.as_view(), name='create-wishlist'),
    path('', WishlistList.as_view(), name='wishlist-all'),
    path('<uuid:pk>/', WishListdetails.as_view(), name='wishlist-details'),
    path('<uuid:pk>/update/', WishListdetails.as_view(), name='wishlist-update'),
    path('<uuid:pk>/delete/', WishListdetails.as_view(), name='wishlist-delete'),
    
]
