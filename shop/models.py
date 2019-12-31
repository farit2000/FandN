from django.db import models
from django.contrib.postgres.fields import JSONField


class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.TextField()
    phone = models.CharField(max_length=12, primary_key=True)


class Product(models.Model):
    price = models.IntegerField()
    description = models.TextField()
    attributes = JSONField()


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    create_date = models.DateTimeField()