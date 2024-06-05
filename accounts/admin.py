from django.contrib import admin

# Register your models here.
from .models import *


class ProductAdmin(admin.ModelAdmin):
    """User profile admin."""

    list_display = ("id", "user", "name", 'quantity','price', 'image', 'category' )
    search_fields = ("price", "name", 'category',)
    # ordering = ("-created_at",)


# admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(User)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview)
admin.site.register(Order)
admin.site.register(ProductCategory)
admin.site.register(Cart)