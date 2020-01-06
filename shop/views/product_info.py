from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from shop.models import Product
from shop.cart import Cart


class ProductInfo(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        is_activated_btn = product in Cart(request)
        print(is_activated_btn)
        return render(request, 'shop/product.html',
                      context={'product': product, 'is_activated_btn': is_activated_btn})

    def post(self, request, slug):
        cart = Cart(request)
        product = Product.objects.get(slug=slug)
        quantity = request.POST.get('quantity')
        cart.add(product, quantity)
        return HttpResponse(status=200)
