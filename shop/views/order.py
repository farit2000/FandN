from django.shortcuts import render, get_object_or_404
from shop import cart
from shop.models import Product, Order, ProductInOrder


def order_index(request):
    basket = cart.Cart(request)
    return render(request, 'shop/order.html', {'cart': basket.__iter__(), 'total_price': basket.get_total_price})