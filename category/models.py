from django.db import models
from datetime import timezone

# Create your models here.
class ProductCategory(models.Model):
    user = models.ForeignKey('accounts.User', models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'product_category'

class ProductSubCategory(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    parent_category = models.ForeignKey('ProductCategory', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'product_sub_category'