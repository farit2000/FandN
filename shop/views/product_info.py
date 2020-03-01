from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views import View
from shop.models import Product, ProductOptions
from shop.cart import Cart


class ProductInfo(View):
    def get(self, request, slug):
        product = Product.objects.prefetch_related('option_groups__options').get(slug=slug)
        groups = product.option_groups.all()
        opts = []
        for group in groups:
            for opt in group.options.all():
                opts.append(opt)
        opts_json = mark_safe(serializers.serialize('json', opts))
        return render(request, 'shop/product.html',
                      context={'product': product,
                               'opt_groups': groups,
                               'opts_data': opts_json})

    def post(self, request, slug):
        cart = Cart(request)
        product = Product.objects.get(slug=slug)
        quantity = request.POST.get('quantity')
        options = ProductOptions.objects.filter(id__in=request.POST.getlist('options'))
        cart.add(product, options,  quantity)
        return HttpResponse(status=200)
