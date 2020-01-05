from collections import namedtuple
from django.shortcuts import render
from shop.models import Product

product_image = namedtuple('Product_image', ['product', 'first_image'])


def index(request):
    # all_product = [product_image(i, i.images.first().image) for i in Product.objects.all()]
    # if len(all_product) % 2 != 0:
    #     all_product.append(product_image(None, None))
    # all_product_in_pairs = zip(all_product[::2], all_product[1::2])
    return render(request, 'shop/index.html', context={'products': Product.objects.all()})
