from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from products.views import ProductListCreateAPIView, ProductDetailAPIView
from search.views import SearchView
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="First Collectionz API",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/accounts/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/accounts/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('cart/', include('cart.urls')),
    path('category/', include('category.urls')),
    path('chatApp/', include('chatApp.urls')),
    path('coupon/', include('coupon.urls')),
    path('orders/', include('orders.urls')),
    path('payment/', include('payment.urls')),
    path('products/', include('products.urls')),
    path('reviews/', include('reviews.urls')),
    path('search/', include('search.urls')),
    path('sort/', include('sort.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('recommendations/', include('recommendations.urls')),
    # path('payment/', include('payment.urls')),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)