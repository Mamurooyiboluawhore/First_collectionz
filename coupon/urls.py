from django.urls import path
from .views import CouponListAPIView, CouponCreateViewAPI


urlpatterns = [
    path('', CouponListAPIView.as_view(), name='coupon-list'),
    path('create-coupon/', CouponCreateViewAPI.as_view(), name='create-coupon')
]