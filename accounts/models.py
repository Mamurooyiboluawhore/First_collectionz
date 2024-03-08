from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
import uuid



class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """
    def create_user(self, email, name, password=None):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """ Create a new superuser profile """
        user = self.create_user(email,name, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Database model for users in the system """
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    otp = models.CharField(max_length=6, null=True, blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        """ Return string representation of our user """
        return self.email


class Cart(models.Model):
    id = models.UUIDField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey("Product", models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_At', auto_now_add=True)
    updated_at = models.DateTimeField(db_column='updated_At',  auto_now_add=True)


    class Meta:
        db_table = 'cart'

class Complaint(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    complaint_text = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=225, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_At', blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_At', blank=True, null=True)

    class Meta:
        db_table = 'complaint'


class ComplaintComment(models.Model):
    complaint = models.ForeignKey('Complaint', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_At', blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_At', blank=True,  null=True)

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
    id = models.UUIDField(primary_key=True)
    customer = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    vat = models.DecimalField(db_column='VAT', max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.TextField() 
    createdat = models.DateTimeField(db_column='created_At', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updated_At', blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'order'


class OrderItems(models.Model):
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    promo = models.ForeignKey('Promotion', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(db_column='created_At', blank=True, null=True)
    updated_at = models.DateTimeField(db_column='updated_At', blank=True, null=True )
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
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)
    sub_category = models.ForeignKey('ProductSubCategory', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'product'


class ProductCategory(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, null=True, blank=True)
    name = models.CharField(max_length=300, blank=True, null=True)
    created_at = models.DateTimeField(db_column='create_At', blank=True, null=True)

    class Meta:
        db_table = 'product_category'

class ProductSubCategory(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    parent_category = models.ForeignKey('ProductCategory', models.DO_NOTHING, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)

    class Meta:
        db_table = 'product_sub_category'



# class ProductReview(models.Model):
#     product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
#     comment = models.TextField(blank=True, null=True)
#     reply = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
#     createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)

#     class Meta:
#         db_table = 'product_review'

class ProductReview(models.Model):
    product = models.ForeignKey('Product', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    reply = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)

    class Meta:
        db_table = 'product_review'
class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    url = models.CharField(max_length=255)

    class Meta:
        db_table = 'product_image'


class PromoProduct(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    promo = models.ForeignKey('Promotion', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.

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
    createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'promotion'


class Role(models.Model):
    name = models.CharField(max_length=225, blank=True, null=True)
    class Meta:
        db_table = 'role'



# class User(models.Model):
#     id = models.UUIDField(primary_key=True)
#     username = models.CharField(max_length=255, blank=True, null=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     role = models.ForeignKey(Role, models.DO_NOTHING, blank=True, null=True)
#     section_order = models.TextField(blank=True, null=True)
#     password = models.CharField(max_length=255, blank=True, null=True)
#     provider = models.CharField(max_length=255, blank=True, null=True)
#     phone_number = models.CharField(max_length=255, blank=True, null=True)
#     is_verified = models.BooleanField(blank=True, null=True)
#     two_factor_auth = models.BooleanField(blank=True, null=True)
#     location = models.CharField(max_length=255, blank=True, null=True)
#     country = models.CharField(max_length=255, blank=True, null=True)
#     profile_pic = models.TextField(blank=True, null=True)
#     profile_cover_photo = models.TextField(blank=True, null=True)
#     createdat = models.DateTimeField(db_column='createdAt', blank=True, null=True)
#     last_login = models.DateTimeField(blank=True, null=True)
#     refresh_token = models.TextField(blank=True, null=True)
#     is_seller = models.BooleanField(blank=True, null=True)
#     slug = models.CharField(max_length=255, blank=True, null=True)
#     two_fa_code = models.CharField(blank=True, null=True)

#     class Meta:
#         db_table = 'user'
        


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
    createdat = models.DateTimeField(db_column='createdAt', default=timezone.now, blank=True, null=True)
    updatedat = models.DateTimeField(db_column='updatedAt', default=timezone.now, blank=True, null=True)

    class Meta:
        db_table = 'wishlist'
