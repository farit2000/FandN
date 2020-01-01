from django.db import models
from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver
from django.db.models.signals import post_save


class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=12, primary_key=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    images = models.ImageField(upload_to='shop/static/media/products_images')
    attributes = JSONField(null=True, blank=True)

    def __str__(self):
        return "%s, price: %s" % (self.name, self.price)


class Order(models.Model):
    ORDER_STATUSES = (
        ('NE', 'NEW'),
        ('HA', 'HANDLING'),
        ('CA', 'CANCELED'),
        ('CO', 'COMPLITED'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='orders')
    create_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField(default=0)
    status = models.CharField(max_length=2, choices=ORDER_STATUSES, default='NE')

    def __str__(self):
        return "%s, sum: %s" % (self.client, self.total_price)


class ProductInOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE, default=0)

    def save(self, *args, **kwargs):
        self.total_price = self.count * self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return "%s, sum: %s" % (self.product, self.total_price)


@receiver(post_save, sender=ProductInOrder)
def count_total_order_price(sender, instance, **kwargs):
    all_products_in_order = ProductInOrder.objects.filter(order=instance.order)
    count = 0
    for product in all_products_in_order:
        count += product.total_price
    instance.order.total_price = count
    instance.order.save(force_update=True)
