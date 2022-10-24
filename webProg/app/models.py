from django.db import models


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=40, blank=False, default='')
    author = models.CharField(max_length=30, blank=False, default='')
    amount = models.FloatField(default=0.0, blank=False)

    class Meta:
        db_table = 'books'


class User(models.Model):
    login = models.CharField(max_length=255, blank=False, default='')
    password = models.CharField(max_length=128, blank=False, default='')
    email = models.CharField(max_length=255, blank=False, default='')
    handle = models.CharField(max_length=255, blank=False, default='')
    role = models.CharField(max_length=255, blank=False, default='')

    class Meta:
        db_table = 'users'
