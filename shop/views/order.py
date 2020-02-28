from django.shortcuts import render, get_object_or_404
from shop import cart
from shop.models import Product, Order, ProductInOrder, Client, ProductOptions
from ..forms import ClientForm


def order_index(request):
    basket = cart.Cart(request)
    if request.method == "POST":
        phone = request.POST['phone']
        form = ClientForm(request.POST)
        is_form_valid = form.is_valid()
        if not Client.objects.filter(phone=phone).exists():
            if is_form_valid:
                client = form.save()
                Order.objects.create(client=client, total_price=basket.get_total_cart_price())
                order = Order.objects.get(client=client)
                write_to_order(basket, order)
                basket.clear()
                return render(request, 'shop/success.html', {})
        else:
            client = Client.objects.get(phone=phone)
            Order.objects.create(client=client, total_price=basket.get_total_cart_price())
            order = Order.objects.filter(client=client).order_by("-id")[0]
            write_to_order(basket, order)
            basket.clear()
            return render(request, 'shop/success.html', {})
    form = ClientForm()
    return render(request, 'shop/order.html', {'basket': iter(basket), 'total_price': basket.get_total_cart_price(),
                                               'form': form})


def write_to_order(basket, order):
    for item in basket:
        ProductInOrder.objects.create(product=Product.objects.get(id=item['product_id']),
                                      count=item['quantity'],
                                      total_price=item['product_total_price'],
                                      order=order).options.set(ProductOptions.objects.filter(id__in=item['option_ids']))
