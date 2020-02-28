from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from shop import cart
from shop.models import Product


def index(request):
    basket = cart.Cart(request)
    return render(request, 'shop/test.html', {'basket': iter(basket)})