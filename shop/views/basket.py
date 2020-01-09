from django.shortcuts import render, get_object_or_404
from shop import cart
from shop.models import Product
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    basket = cart.Cart(request)
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        if int(action) == 1:
            basket.add(get_object_or_404(Product, slug=product_id))
        elif int(action) == -1:
            basket.reduce(get_object_or_404(Product, slug=product_id))
        elif int(action) == 0:
            basket.remove(get_object_or_404(Product, slug=product_id))
        basket_total_price = basket.get_total_price()
        return render(request, 'shop/basket.html', {'cart': basket.__iter__(), 'total_price': basket_total_price})

    # basket.add(get_object_or_404(Product, id=5))
    # basket.add(get_object_or_404(Product, id=7))
    # basket.add(get_object_or_404(Product, id=12))
    # basket.add(get_object_or_404(Product, id=17))
    # basket.add(get_object_or_404(Product, id=18))
    # basket.add(get_object_or_404(Product, id=20))
    # basket.remove(product=get_object_or_404(Product, id=5))
    basket_total_price = basket.get_total_price()
    return render(request, 'shop/basket.html', {'cart': basket.__iter__(), 'total_price': basket_total_price})