from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=40, blank=False, default='')
    author = models.CharField(max_length=30, blank=False, default='')
    amount = models.IntegerField(default=0, blank=False)
    price = models.FloatField(default=0.0, blank=False)

    class Meta:
        db_table = 'books'


class User(models.Model):
    login = models.CharField(max_length=255, blank=False, default='')
    password = models.CharField(max_length=128, blank=False, default='')
    email = models.CharField(max_length=255, blank=False, default='')
    handle = models.CharField(max_length=255, blank=False, default='')
    role = models.CharField(max_length=255, blank=False, default='')

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    class Meta:
        db_table = 'users'


class CartItem(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, blank=False)

    class Meta:
        db_table = 'cart_items'


class Order(models.Model):
    order_number = models.IntegerField(default=0, blank=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0, blank=False)
    price = models.FloatField(default=0.0, blank=False)

    class Meta:
        db_table = 'orders'
