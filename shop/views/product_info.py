from django.shortcuts import render
from shop.models import Product


def index(request, slug):
    product = Product.objects.get(slug=slug)
    return render(request, 'shop/product.html', context={'product': product})

