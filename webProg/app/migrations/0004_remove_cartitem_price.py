# Generated by Django 4.1.1 on 2022-11-01 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_book_price_cartitem_price_alter_book_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='price',
        ),
    ]
