from django.urls import path
from .views import Payment

urlpatterns = [
    path('initiate/', Payment.as_view(), name='payment_initiate'),
    path('confirm/', Payment.as_view(), name='payment_confirm'),
]
