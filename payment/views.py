from core import settings as core_settings
from rave_python import Rave, RaveExceptions, Misc
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from  rest_framework.decorators import action
from accounts.models import Order, User
import requests
from orders.serializers import OrderCreateSerializer, OrderItemsSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
import uuid


import os


class Payment(APIView):
    """
    Handle payment initiation and confirmation.
    """
    def initiate_payment(amount, email, order_id):
        """
        Initiate the payment process with Flutterwave.
        """
        url = "https://api.flutterwave.com/v3/payments"
        headers = {
            "Authorization": f"Bearer {core_settings.FLW_SEC_KEY}"    
        }
        redirect_url = core_settings.FLW_REDIRECT_URL + f"?o_id={order_id}"
        data = {
            "tx_ref": str(uuid.uuid4()),
            "amount": str(amount),  
            "currency": "USD",
            "redirect_url": redirect_url,
            "meta": {
                "consumer_id": 23,
                "consumer_mac": "92a3-912ba-1192a"
            },
            "customer": {
                "email": email,
                "phonenumber": "080****4528",
                "name": "Yemi Desola"
            },
            "customizations": {
                "title": "Pied Piper Payments",
                "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png"
            }
        }
    

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            return Response(response_data, status=status.HTTP_200_OK)
    
        except requests.RequestException as err:
            print(f"Payment initiation failed: {err}")
            response = {
                'error': "Payment initiation failed",
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

    def post(self, request, pk):
        """
        Handle POST request to initiate payment.
        """
        try:
            order = get_object_or_404(Order, pk=pk)
            amount = order.total_price
            email = request.user.email
            order_id = order.id
            return self.initiate_payment(amount, email, order_id)
        except Exception as e:
            print(f"Error initiating payment: {e}")
            data = {
                'error': 'Error initiating payment',
                'error': True,
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR
            }
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def confirm_payment(self, request):
        """
        Handle confirmation of payment.
        """
        order_id = request.GET.get("o_id")
        try:
            order = Order.objects.get(id=order_id)
            order.pending_status = "C"
            order.save()
            serializer = OrderSerializer(order)
            data = {
                "msg": "Payment was successful",
                "status": status.HTTP_200_OK,
                "data": serializer.data
            }
            return Response(data)
        except Order.DoesNotExist:
            response = {
                'error': "Order not found",
                'status': status.HTTP_404_NOT_FOUND,
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error confirming payment: {e}")
            response = {
                "error": "Error confirming payment.",
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)