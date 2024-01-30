from django.views import View
from django.http import JsonResponse
from accounts.models import Product



class SearchView(View):
    def search_views(self, request, *args, **kwargs):
        query = request.GET.get('q')
        products = Product.objects.filter(title__icontain=query, description__icontain=query).order_by('-date')

        context = {
            "products": products,
            "query": query
        }
        return JsonResponse(context)