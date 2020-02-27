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
        product_id = str(product.id)
        option_ids = []
        options_price = 0
        for option in options:
            option_ids.append(str(option.id))
            options_price += option.delta
        if str(product_id) + str(option_ids) not in self.cart.keys():
            self.cart[str(product_id) + str(option_ids)] = {
                'quantity': int(quantity),
                'name': product.name,
                'price': int(product.price) + int(options_price),
                'main_image': str(product.main_option.images.first())
            }
        else:
            prev_quantity = self.cart[str(product_id) + str(option_ids)]
            self.cart[str(product_id) + str(option_ids)]['quantity'] = int(prev_quantity) + int(quantity)
        self.save()

    def reduce(self, product, options, quantity=1):
        product_id = str(product.id)
        option_ids = []
        for option in options:
            option_ids.append(str(option.id))
        self.cart[product_id, option_ids] -= quantity
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product, options):
        product_id = str(product.id)
        option_ids = []
        for option in options:
            option_ids.append(str(option.id))
        if (product_id, option_ids) in self.cart:
            del self.cart[product_id, option_ids]
            self.save()

    def __contains__(self, product, options):
        product_id = str(product.id)
        option_ids = []
        for option in options:
            option_ids.append(str(option.id))
        return (product_id, option_ids) in list(self.cart.keys())

    def __iter__(self):
        keys = self.cart.keys()
        for key in keys:
            product = Product.objects.get(id=key[0])
            options = ProductOptions.objects.filter(id__in=key[1])
            self.cart[key[0], key[1]]['product_id'] = key[0]
            self.cart[key[0], key[1]]['product_name'] = product.name
            self.cart[key[0], key[1]]['product_slug'] = product.slug
            self.cart[key[0], key[1]]['product_price'] = product.price
            self.cart[key[0], key[1]]['product_description'] = product.description
            self.cart[key[0], key[1]]['product_image'] = product.main_option.images.first()
            self.cart[key[0], key[1]]['product_attributes'] = product.attributes
            self.cart[key[0], key[1]]['product_category'] = product.category.name
            self.cart[key[0], key[1]]['options'] = options
            options_ids = []
            options_sum_delta = 0
            option_name_and_values = {}
            for option in options:
                options_ids.append(option.id)
                options_sum_delta += option.delta
                option_name_and_values[option.option_name] = option.option_value
            self.cart[key[0], key[1]]['option_ids'] = options_ids
            self.cart[key[0], key[1]]['option_sum_delta'] = options_sum_delta
            self.cart[key[0], key[1]]['option_name_and_values'] = option_name_and_values

        for item in self.cart.values():
            item['product_price'] = int(item['price'])
            item['option_sum_delta'] = int(item['option_sum_delta'])
            item['price'] = int(item['product_price']) + int(item['option_sum_delta'])
            item['total_price'] = (item['price'] + item['option_sum_delta']) * int(item['quantity'])
            yield item

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_cart_price(self):
        return sum(int(item['total_price']) for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
