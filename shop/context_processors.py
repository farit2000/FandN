from shop.cart import Cart


def get_bag(request):
    cart = Cart(request)
    bag_quantity = len(cart)
    if not bag_quantity:
        bag_quantity = ''
    return {'bag_quantity': bag_quantity, 'cart': iter(cart)}

