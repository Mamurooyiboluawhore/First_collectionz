from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from products.serializers import ProductSerializer

class SearchView(APIView):
    serializer_class = ProductSerializer
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        products = Product.objects.filter(name__icontains=query).order_by('-createdat')

        # Use serializer_class to instantiate the serializer
        serializer = self.serializer_class(products, many=True, context={'request': request})

        context = {
            "products": serializer.data,
            "query": query
        }
        return Response(context, status=status.HTTP_200_OK)
