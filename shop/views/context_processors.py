from shop.cart import Cart


def get_bag_quantity(request):
    bag_quantity = len(Cart(request).cart.keys())
    if not bag_quantity:
        bag_quantity = ''
    return {'bag_quantity': bag_quantity}
