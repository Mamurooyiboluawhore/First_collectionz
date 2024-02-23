from django.urls import path
from .views import SortViewApi


urlpatterns = [
    path(' ', SortViewApi.as_view(), name='sort-products')

]
