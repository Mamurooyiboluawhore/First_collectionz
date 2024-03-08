from accounts.models import Coupon
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CouponSerializer



class CouponCreateViewAPI(APIView):
    def post(self, request):
        try:
            serializer = CouponSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response = {
                    "message": "Coupon successfully created",
                    "status_code": status.HTTP_201_CREATED,
                    "data": serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CouponListAPIView(APIView):
    def get(self, request):
        try:
            coupon = Coupon.objects.all()
            serializer = CouponSerializer(coupon)
            response = {
                'status_code' : status.HTTP_200_OK,
                'message': "list of all coupons",
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)