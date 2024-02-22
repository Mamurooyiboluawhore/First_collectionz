from django.urls import path
from .views import SortViewApi


ulrpatterns = [
    path(' ', SortViewApi.as_view(), name='sort-products')

]
