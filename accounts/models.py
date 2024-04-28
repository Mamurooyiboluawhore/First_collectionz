from django.db import models
# from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
import uuid



class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """
    def create_user(self, email, password=None, **extra_fields):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """ Create a new superuser profile """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        # u?ser = self.create_user(email, password)
        
        # user.save(using=self._db)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """ Database model for users in the system """
    username = None
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at =models.DateTimeField(auto_now_add=True)

    objects = UserProfileManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        """ Return string representation of our user """
        return self.email


	

class Cart(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey("Product", models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart'

class Complaint(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    complaint_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=225, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'complaint'


class ComplaintComment(models.Model):
    complaint = models.ForeignKey('Complaint', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'complaint_comment'


class Coupon(models.Model):
    seller = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    limit = models.IntegerField(blank=True, null=True)
    percentage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coupon_code = models.CharField(max_length=20, blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'coupon'


class Favourite(models.Model):
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'favourite'


class Images(models.Model):
    url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'images'


class NotificationConfirmation(models.Model):
    mail_id = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'notification_confirmation'


class NotificationSetting(models.Model):
    email_summary = models.BooleanField(blank=True, null=True)
    special_offers = models.BooleanField(blank=True, null=True)
    community_update = models.BooleanField(blank=True, null=True)
    follow_update = models.BooleanField(blank=True, null=True)
    new_messages = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'notification_setting'


class Order(models.Model):
    PAYMENT_STATUS_PENDING='P'
    PAYMENT_STATUS_PROCESSING='PR'
    PAYMENT_STATUS_COMPLETE='C'
    PAYMENT_STATUS_FAILED='F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'pending'),
        (PAYMENT_STATUS_COMPLETE, 'complete'),
        (PAYMENT_STATUS_FAILED, 'failed'),
    ]
    id = models.UUIDField(primary_key=True)
    customer = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    vat = models.DecimalField(db_column='VAT', max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.TextField() 
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    promo = models.ForeignKey('Promotion', models.DO_NOTHING, blank=True, null=True)
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    
    
   
    class Meta:
        db_table = 'order'

    def __str__(self):
        return self.pending_status
    
    @property 
    def total_price(self):
        items = self.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total


class OrderItems(models.Model):
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    promo = models.ForeignKey('Promotion', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(db_column='deleted_At', blank=True, null=True)
    is_delete = models.BooleanField(blank=True, null=True)
    status = models.TextField(blank=True, null=True) 

    class Meta:
        db_table = 'order_items'


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50)
    paid = models.BooleanField(default=False)
    user =  models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'payment'


class Product(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    quantity = models.BigIntegerField()
    category = models.ForeignKey('ProductCategory', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    admin_status = models.TextField(blank=True, null=True)
    is_deleted = models.TextField(blank=True, null=True)
    rating = models.ForeignKey('UserProductRating', models.DO_NOTHING, blank=True, null=True)
    is_published = models.BooleanField()
    currency = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    sub_category = models.ForeignKey('ProductSubCategory', models.DO_NOTHING, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', null=False, blank=True)

    class Meta:
        db_table = 'product'


class ProductCategory(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(default=timezone.now)
    class Meta:
        db_table = 'product_category'

class ProductSubCategory(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    parent_category = models.ForeignKey('ProductCategory', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'product_sub_category'


class ProductReview(models.Model):
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    reply = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_review'



class PromoProduct(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    promo = models.ForeignKey('Promotion', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'promo_product'

class Promotion(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    code = models.CharField(max_length=255)
    promotion_type = models.CharField(max_length=255)
    discount_type = models.TextField(blank=True, null=True)  # This field type is a guess.
    quantity = models.BigIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    maximum_discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'promotion'
        

class UserProductRating(models.Model):
    user_id = models.UUIDField(blank=True, null=True)
    product_id = models.UUIDField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'user_product_rating'


class Wishlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'wishlist'
