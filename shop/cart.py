from django.conf import settings
from shop.models import Product, Image


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': int(quantity),
                                     'name': product.name,
                                     'price': int(product.price),
                                     'main_image': str(product.images.first().image)}
        else:
            prev_quantity = self.cart[product_id]['quantity']
            self.cart[product_id]['quantity'] = int(prev_quantity) + int(quantity)
        self.save()

    def reduce(self, product):
        product_id = str(product.id)
        self.cart[product_id]['quantity'] -= 1
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __contains__(self, product):
        return str(product.id) in list(self.cart.keys())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['id'] = product.slug
            self.cart[str(product.id)]['name'] = product.name
            self.cart[str(product.id)]['price'] = product.price
            self.cart[str(product.id)]['description'] = product.description
            self.cart[str(product.id)]['image'] = str(Image.objects.filter(product_id=product.id).first().image)
            self.cart[str(product.id)]['attributes'] = product.attributes
            self.cart[str(product.id)]['category'] = product.category

        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = int(item['price']) * int(item['quantity'])
            yield item

    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())

    def get_total_price(self):
        return sum(int(item['price']) * int(item['quantity']) for item in
                   self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True