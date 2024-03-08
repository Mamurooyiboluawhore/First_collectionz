from django.urls import path
from .views import CouponListAPIView


urlpatterns = [
    path('', CouponListAPIView.as_view(), name='coupon-list'),
]