from django import template
from shop.models import Product

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.simple_tag(name='get_slug_by_id')
def get_slug_by_id(id):
    return Product.objects.get(id=id).slug

