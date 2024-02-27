from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import Product
from .serializers import SortSerializer


class SortViewApi(APIView):
    def get(self, request):
        try:
            sort = Product.objects.all().order_by('price', 'category', 'createdat')
            serializer = SortSerializer(sort, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)