# Generated by Django 5.1.2 on 2024-11-28 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_customer_phone_seller_joined_on_delete_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='phone',
            new_name='mobile',
        ),
    ]