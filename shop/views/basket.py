from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from shop import cart
from shop.models import Product
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    basket = cart.Cart(request)
    if request.method == "POST":
        print(request.POST)
        product_id = request.POST.get('product_id')
        action = int(request.POST.get('action'))
        if action == 1:
            delta = int(request.POST.get('delta'))
            if delta > 0:
                basket.add(get_object_or_404(Product, id=product_id), quantity=delta)
            elif delta < 0:
                basket.reduce(get_object_or_404(Product, id=product_id), quantity=-delta)
        elif action == 0:
            basket.remove(get_object_or_404(Product, id=product_id))
        return HttpResponse(status=200)
    basket_total_price = basket.get_total_price()
    return render(request, 'shop/cart.html', {'cart': iter(basket), 'total_price': basket_total_price})