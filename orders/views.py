from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from accounts.models import Order
from .serializers import OrderSerializers
from rest_framework.permissions import IsAuthenticated

class ProductListCreateAPIView(APIView):
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
