from django.shortcuts import render, get_object_or_404
from shop import cart
from shop.models import Product, Order, ProductInOrder, Client
from ..forms import ClientForm


def order_index(request):
    basket = cart.Cart(request)
    if request.method == "POST":
        phone = request.POST['phone']
        form = ClientForm(request.POST)
        if not Client.objects.filter(phone=phone).exists():
            if form.is_valid():
                client = form.save()
                Order.objects.create(client=client, total_price=basket.get_total_price())
                order = Order.objects.get(client=client)
                for item in basket.__iter__():
                    ProductInOrder.objects.create(product=Product.objects.get(slug=item['id']), count=item['quantity'],
                                                  total_price=item['price'], order=order)
                basket.clear()
                return render(request, 'shop/index.html', {})
        else:
            client = Client.objects.get(phone=phone)
            Order.objects.create(client=client, total_price=basket.get_total_price())
            order = Order.objects.filter(client=client).order_by("-id")[0]
            for item in basket.__iter__():
                ProductInOrder.objects.create(product=Product.objects.get(slug=item['id']), count=item['quantity'],
                                              total_price=item['price'], order=order)
            basket.clear()
            return render(request, 'shop/index.html', {})
    form = ClientForm()
    return render(request, 'shop/order.html', {'cart': basket.__iter__(), 'total_price': basket.get_total_price,
                                               'form': form})

