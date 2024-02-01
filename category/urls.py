from django.urls import path
from .views import CategoryCreateAPIView, CategoryDetailAPIViews


urlpatterns = [
    path('', CategoryCreateAPIView.as_view(), name='category-list-create'),
    path('<uuid:pk>/', CategoryDetailAPIViews.as_view(), name='category-detail'),
    path('<uuid:pk>/details/', CategoryDetailAPIViews.as_view(), name='category-details'),
    path('<uuid:pk>/delete/', CategoryDetailAPIViews.as_view(), name='category-delete'),
]
