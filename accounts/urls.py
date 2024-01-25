from django.urls import path
from . import views
from products.views import ProductListCreateAPIView, ProductDetailAPIViews
from search.views import SearchView
# from search import SearchView



urlpatterns = [
	path('create/', views.user_create, name='user_create'),
	path('list/', views.user_list_viewset, name='user_list'),
	path('<int:pk>/', views.user_detail_viewset, name='user_detail_viewset'),
	path('', views.user_detail, name='user_detail'),
	path('<int:pk>/update/', views.user_update_viewset, name='user_update'),
	path('change-password/', views.change_password, name='change_password'),
]