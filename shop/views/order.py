from django.shortcuts import render
from shop import cart
from shop.models import Product, Order, ProductInOrder, Client, ProductOptions
from ..forms import ClientForm, OrderForm
from django.core.mail import send_mail
from django.template import loader


def order_index(request):
    basket = cart.Cart(request)
    if request.method == "POST":
        phone = request.POST['phone']
        client_form = ClientForm(request.POST)
        order_form = OrderForm(request.POST)
        is_form_valid = client_form.is_valid() & order_form.is_valid()
        if not Client.objects.filter(phone=phone).exists():
            if is_form_valid:
                client = client_form.save()
                Order.objects.create(client=client, total_price=basket.get_total_cart_price(),
                                     addition=order_form.cleaned_data['addition'])
                order = Order.objects.get(client=client)
                write_to_order(basket, order, client_form.cleaned_data['email'])
                return render(request, 'shop/success.html', {})
        else:
            client = Client.objects.get(phone=phone)
            if not (client.first_name == client_form.cleaned_data['first_name'] and
                    client.last_name == client_form.cleaned_data['last_name'] and
                    client_form.email == client_form.cleaned_data['email']):
                client.first_name = client_form.cleaned_data['first_name']
                client.last_name = client_form.cleaned_data['last_name']
                client.email = client_form.cleaned_data['email']
                client.save(update_fields=["first_name", "last_name", "email"])
            Order.objects.create(client=client, total_price=basket.get_total_cart_price(),
                                 addition=order_form.cleaned_data['addition'])
            order = Order.objects.filter(client=client).order_by("-id")[0]
            write_to_order(basket, order, client_form.cleaned_data['email'])
            return render(request, 'shop/success.html', {})
    client_form = ClientForm()
    order_form = OrderForm()
    return render(request, 'shop/order.html', {'basket': basket, 'total_price': basket.get_total_cart_price(),
                                               'client_form': client_form, 'order_form': order_form})


def write_to_order(basket, order, client_email):
    for item in basket:
        ProductInOrder.objects.create(product=Product.objects.get(id=item['product_id']),
                                      count=item['quantity'],
                                      total_price=item['product_total_price'],
                                      order=order).options.set(ProductOptions.objects.filter(id__in=item['option_ids']))
        html_message = loader.render_to_string(
            './shop/email.html',
            {
                'basket': basket,
            }
        )
        send_mail('Заказ в интернет магазине F&N', 'Благодарим вас за проявленный интерес к нашей продукции',
                  'fandn.market@gmail.com', [client_email], html_message=html_message)
        # send_mail('Новый заказ!!!', 'Новый заказ на сайте от клиета {}'.format(client_email), 'fandn.market@gmail.com',
        #           ['farit.schamardanov1@gmail.com'], html_message = )
    basket.clear()
