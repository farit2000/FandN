from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from shop import cart
from shop.models import Product, ProductOptions
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    basket = cart.Cart(request)
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        option_ids = request.POST.getlist('option_ids[]')
        action = int(request.POST.get('action'))
        if action == 1:
            delta = int(request.POST.get('delta'))
            if delta > 0:
                basket.add(get_object_or_404(Product, id=product_id),
                           ProductOptions.objects.filter(id__in=option_ids),
                           quantity=delta)
            elif delta < 0:
                basket.reduce(get_object_or_404(Product, id=product_id),
                              ProductOptions.objects.filter(id__in=option_ids),
                              quantity=-delta)
        elif action == 0:
            basket.remove(get_object_or_404(Product, id=product_id), ProductOptions.objects.filter(id__in=option_ids))
        return HttpResponse(status=200)
    basket_total_price = basket.get_total_cart_price()
    return render(request, 'shop/basket.html', {'basket': iter(basket), 'total_price': basket_total_price})