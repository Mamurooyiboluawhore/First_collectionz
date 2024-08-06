from django.db import models
import uuid
from products.models import Product
from accounts.models import User
# Create your models here.
class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'wishlist'
