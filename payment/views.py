from rave_python import Rave, RaveExceptions, Misc
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import Order, User
import requests
from .serializers import OrderCreateSerializer, OrderItemsSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated
import uuid


import os

rave = Rave(os.getenv("Public_key"))

# Payload with pin
payload = {
  "cardno": "5438898014560229",
  "cvv": "890",
  "expirymonth": "09",
  "expiryyear": "19",
  "amount": "10",
  "email": "user@gmail.com",
  "phonenumber": "0902620185",
  "firstname": "temi",
  "lastname": "desola",
  "IP": "355426087298442",
}

try:
    res = rave.Card.charge(payload)

    if res["suggestedAuth"]:
        arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

        if arg == "pin":
            Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
        if arg == "address":
            Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
        
        res = rave.Card.charge(payload)

    if res["validationRequired"]:
        rave.Card.validate(res["flwRef"], "")

    res = rave.Card.verify(res["txRef"])
    print(res["transactionComplete"])

except RaveExceptions.CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except RaveExceptions.TransactionValidationError as e:
    print(e.err)
    print(e.err["flwRef"])

except RaveExceptions.TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])


def initiate_payment(amount, email, order_id):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {
        "Authorization": f"Bearer {os.getenv('Secret_key')}"    
    }
    
    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount), 
        "currency": "USD",
        "redirect_url": "http:/127.0.0.1:8000/api/orders/confirm_payment/?o_id=" + order_id,
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
        response_data = response.json()
        return Response(response_data)
    
    except requests.exceptions.RequestException as err:
        print("the payment didn't go through")
        return Response({"error": str(err)}, status=500)
    

@csrf_exempt
@api_view(['POST'])
def confirm_payment(request, o_id):
    """
    Confirm a payment made to an order using Flutterwave Transaction Reference (tx_ref).
    The tx_ref is sent in the redirect URL when the user makes a successful payment on Flutterwave.
    This view returns the status of that transaction and updates the Order model with the appropriate status if it was successful or failed.
    This view returns a JSON object with information about the transaction if it exists and has not been confirmed yet.
    This view returns the transaction details if it exists and has not been confirmed yet.
    If the transaction does not exist or has already been confirmed, it will return a message saying so.
    :param request: HTTP Request from client
    :type request: HttpRequest
    :param o_id: Order ID of the order being paid for
    :type o_id: int
    :return: JSON object containing transaction data if it exists and hasn't been confirmed
    Message stating that the transaction doesn't exist or has been confirmed
    :rtype: JsonResponse
    """
    url = f"https://api.flutterwave.com/v3/transactions/{o_id}"
    headers = {"Authorization":"Bearer FLWSECK_TEST-d6fadbebeccddc9cd2bfbd9eeaeff3fd"} #
    params = {'flw_test': True}
    try:
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200:
            data = resp.json()
            if 'data' in data and len(data['data']) > 0:
                trans = data['data'][0]
                if trans['meta']['verification']['status'] != 'successful':
                    return Response({"message": "Transaction Not Successfully Verified"}, status=400)
                elif 'message' in data:
                    return Response(data)
                else:
                    return Response(trans)
            
    except Exception as e:
        return Response({"Error":str(e)})
            
