from .views import *
from django.urls import path

urlpatterns = [
    path('recommendations/<uuid:product_id>/', Recommendation.as_view(), name='similar-products'),
]
