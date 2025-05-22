from django.conf import settings

from apps.property.models import Property


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        for p in self.cart.keys():
            self.cart[str(p)]['property'] = Property.objects.get(pk=p)

        for item in self.cart.values():
            item['total_price'] = item['property'].price * item['quantity']

            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, property_id, quantity=1, update_quantity=False):
        property_id = str(property_id)

        if property_id not in self.cart:
            self.cart[property_id] = {'quantity': 1, 'id': property_id}

        if update_quantity:
            self.cart[property_id]['quantity'] += int(quantity)

            if self.cart[property_id]['quantity'] == 0:
                self.remove(property_id)

        self.save()

    def remove(self, property_id):
        if property_id in self.cart:
            del self.cart[property_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_cost(self):
        for p in self.cart.keys():
            self.cart[str(p)]['property'] = Property.objects.get(pk=p)

        return sum(item['quantity'] * item['property'].price for item in self.cart.values())

    def items(self):
        for item in self:
            yield item