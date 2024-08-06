# Generated by Django 4.2.8 on 2024-08-06 14:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=500)),
                ('quantity', models.BigIntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('discount_price', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('admin_status', models.TextField(blank=True, null=True)),
                ('is_deleted', models.TextField(blank=True, null=True)),
                ('is_published', models.BooleanField()),
                ('currency', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, upload_to='product_images/')),
                ('size', models.CharField(blank=True, max_length=100, null=True)),
                ('colours', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.productcategory')),
                ('rating', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.userproductrating')),
                ('sub_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.productsubcategory')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'product',
            },
        ),
    ]