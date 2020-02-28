from django.db import models
from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver
from django.db.models.signals import post_save


class Categories(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s" % self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    attributes = JSONField()
    slug = models.SlugField(unique=True)
    is_available = models.BooleanField()
    # null and blank must be removed, but it's impossible to create objects without them
    main_option = models.OneToOneField('ProductOptions', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s" % self.name


class OptionGroup(models.Model):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, related_name='option_groups', on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.name


class ProductOptions(models.Model):
    option_value = models.CharField(max_length=100)
    delta = models.DecimalField(max_digits=10, decimal_places=2)
    attributes = JSONField(null=True, blank=True)
    is_default = models.BooleanField()
    option_group = models.ForeignKey(OptionGroup, related_name='options', on_delete=models.CASCADE)
    no_compatible_options = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return "%s" % self.option_value


class Image(models.Model):
    options = models.ForeignKey(ProductOptions, on_delete=models.CASCADE, related_name='images')
    path = models.ImageField(upload_to='shop/static/media/products_images')


class Client(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=12, primary_key=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


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
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    options = models.ManyToManyField(ProductOptions)
    count = models.PositiveIntegerField(default=1)
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