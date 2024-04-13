from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import Order
from .serializers import OrderSerializers
from rest_framework.permissions import IsAuthenticated

class OrderListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        """
        Retrieves a list of all orders or an order by its primary key.

        Args:
        request: HTTP request object.
        pk: The primary key of the order to retrieve. Default is None, which means
            all orders will be retrieved.
        format: The requested data format. Default is None.

        Returns:
        Response containing a list of serialized orders or the serialized order if pk is provided.
        """
        try:
            if pk is None:
                # Retrieve all orders
                orders = Order.objects.all()
                serializer = OrderSerializers(orders, many=True)
                return Response(serializer.data)
            else:
                # Retrieve an order by its primary key
                order = get_object_or_404(Order, pk=pk)
                serializer = OrderSerializers(order)
                return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def post(self, request):
        try:
            serializer = OrderSerializers(data=request.data)
            if serializer.is_valid():
            # serializer.is_valid(raise_exception=True)  # Validate input values
                serializer.save()                   # Save new order in database
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, pk):
        try:
            order = Order.objects.get(pk)
            serializer = OrderSerializers(order)
            if serializer.is_valid():
                serializer.update_fields(order, validated_data=request.data)
                serializer.save
                response = {
                    'message': "Order successfully updated",
                    'status': status.HTTP_201_CREATED,
                    'data': serializer.data
                }
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response(status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.delete()
            response ={
                'message': 'Order successfully deleted',
                'status': status.HTTP_204_NO_CONTENT,
            }
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response(status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        