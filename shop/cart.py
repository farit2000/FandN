from django.conf import settings
from shop.models import Product, Image, ProductOptions


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, options, quantity=1):
        option_ids = [option.id for option in options]
        if str(product.id) + str(option_ids) not in self.cart.keys():
            self.cart[str(product.id) + str(option_ids)] = {
                'product_id': product.id,
                'quantity': int(quantity),
                'option_ids': option_ids,
                'product_price': int(product.price),
                'product_price_with_options': int(product.price) + int(sum(option.delta for option in options)),
            }
        else:
            self.cart[str(product.id) + str(option_ids)]['quantity'] += int(quantity)
        self.save()

    def reduce(self, product, options, quantity=1):
        option_ids = [option.id for option in options]
        if str(product.id) + str(option_ids) in self.cart.keys():
            self.cart[str(product.id) + str(option_ids)]['quantity'] -= int(quantity)
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, options):
        option_ids = [option.id for option in options]
        if str(product.id) + str(option_ids) in self.cart.keys():
            del self.cart[str(product.id) + str(option_ids)]
            self.save()

    def __contains__(self, product, options):
        option_ids = [option.id for option in options]
        return str(product.id) + str(option_ids) in self.cart.keys()

    def __iter__(self):
        for product in self.cart.values():
            prod = Product.objects.get(id=product['product_id'])
            options = ProductOptions.objects.filter(id__in=list(product['option_ids']))
            not_default_options = options.filter(is_default=False)
            product['product_name'] = prod.name
            product['product_slug'] = prod.slug
            product['product_description'] = prod.description
            product['product_image'] = prod.main_option.images.first() if not not_default_options \
                else not_default_options.first().images.first()
            product['product_attributes'] = prod.attributes
            product['product_category'] = prod.category
            product['product_total_price'] = product['product_price_with_options'] * product['quantity']
            product['product_option_ids'] = product['option_ids']
            option_name_and_values = {}
            for option in options:
                if not option.is_default:
                    option_name_and_values[option.option_group.name] = option.option_value
            product['option_name_and_value'] = option_name_and_values
        for item in self.cart.values():
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_cart_price(self):
        return sum(item['product_price_with_options'] * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
