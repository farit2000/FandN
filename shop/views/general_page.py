from collections import namedtuple
from django.shortcuts import render
from shop.cart import Cart
from shop.models import Product

product_image = namedtuple('Product_image', ['product', 'first_image'])


def index(request):
    return render(request, 'shop/index.html', context={'products': Product.objects.all()})
