import copy
from decimal import Decimal
from djmarketplace import settings
from app_shops.models import SellItem


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """ Метод добавления товара в корзину """

        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """ Метод для сохранения записи о добавлении товара в корзину """

        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """ Метод для удаления записи из корзины """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """ Метод для итерации по списку товаров """

        cart = copy.deepcopy(self.cart)

        product_ids = cart.keys()
        products = SellItem.objects.filter(id__in=product_ids)

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ Метод для определения число товаров в корзине """

        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """ Метод дл определения итоговой стоимости всех товаров """

        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clean(self):
        """ Метод для очистки корзины """

        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
