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

        # Previous version
        # objs = product.options.all().values('option_name').annotate(count=Count('option_name')).filter(count__gt=1)
        # qs = product.options.filter(option_name__in=[e['option_name'] for e in objs])
        # opts = {}
        # for e in qs:
        #     if e.option_name in opts.keys():
        #         opts[e.option_name].append(e)
        #     else:
        #         opts[e.option_name] = [e]
        # opts_data = mark_safe(serializers.serialize('json', qs))

        return render(request, 'shop/product.html',
                      context={'product': product,
                               'opt_groups': groups,
                               'opts_data': opts_json})

    def post(self, request, slug):
        cart = Cart(request)
        product = Product.objects.get(slug=slug)
        quantity = request.POST.get('quantity')
        options = ProductOptions.objects.filter(id__in=request.POST.getlist('options'))
        print(product, options)
        cart.add(product, options,  quantity)
        return HttpResponse(status=200)
