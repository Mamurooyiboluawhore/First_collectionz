from django.urls import include, path
from .views import OrderListCreateAPIView

urlpatterns = [
    path('', OrderListCreateAPIView.as_view(), name='order-list-create'),
    path('<uuid:pk>/', OrderListCreateAPIView.as_view(), name='get-order'),
    path('<uuid:pk>/update/', OrderListCreateAPIView.as_view(), name='update-order'),
    path('<uuid:pk>/delete/', OrderListCreateAPIView.as_view(), name='delete-order'),
    
]