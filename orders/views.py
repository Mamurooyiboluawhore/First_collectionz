from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import Order, User
from .serializers import OrderCreateSerializer, OrderItemsSerializer, OrderSerializer
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
            if request.user.is_staff:
                # Retrieve all orders if user is staff
                queryset = Order.objects.all().order_by('-date')
                serializer = OrderSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                if pk is None:
                    # Retrieve the logged in user's orders only
                    queryset = Order.objects.filter(user=request.user).order_by('-date')
                    serializer = OrderSerializer(queryset, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    # Retrieve an order by its primary key
                    order = get_object_or_404(Order, pk=pk, user=request.user)
                    serializer = OrderSerializer(order)
                    return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    def post(self, request):
        try:
            serializer = OrderCreateSerializer(data=request.data)
            if serializer.is_valid():
            # serializer.is_valid(raise_exception=True)  # Validate input values
                serializer.save()
                response = {
                    'message':'Order successfully created',
                    'order': serializer.data,
                    'status': status.HTTP_201_CREATED
                }                   # Save new order in database
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def put(self, request, pk):
        try:
            order = Order.objects.get(pk)
            serializer = OrderSerializer(order)
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
