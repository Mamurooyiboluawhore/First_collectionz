# Generated by Django 4.2.8 on 2024-05-08 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_chatmessages'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessages',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Messages'},
        ),
        migrations.AlterModelTable(
            name='chatmessages',
            table=None,
        ),
    ]
