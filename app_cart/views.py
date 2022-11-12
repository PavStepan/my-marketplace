from decimal import Decimal
from app_users.permission.authenticatedpermissionsmixin import AuthenticatedUserPermissionsMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from app_shops.models import SellItem, SoldProduct
from .cart import Cart
from .forms import CartAddProductForm
from django.utils.translation import gettext_lazy as _
import logging

logger = logging.getLogger(__name__)


@require_POST
def cart_add(request, pk):
    cart = Cart(request)
    product = get_object_or_404(SellItem, id=pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, pk):
    cart = Cart(request)
    product = get_object_or_404(SellItem, id=pk)
    cart.remove(product)
    return redirect('cart_detail')


class CartDetail(View, AuthenticatedUserPermissionsMixin):

    def get(self, request, *args, **kwargs):
        form = CartAddProductForm()
        cart = Cart(request)
        if self.request.GET.get('buy') == 'buy_all':
            bonus_use = Decimal(self.request.GET.get('bonus', 0))

            user = self.request.user

            # Начала транзакции
            with transaction.atomic():

                # получаем список товаров к корзине, которые есть на складе
                new_cart = filter(lambda q: q.get('product').number_count > 0, cart)
                correct_total_price = 0
                for item in list(new_cart):
                    quantity = item.get('quantity')
                    product = item.get('product')
                    total_price = cart.get_total_price()

                    # Изменение значения числа товаров на складе
                    product.number_count -= quantity
                    product.save(update_fields=['number_count'])

                    # Запись в модель проданного товара
                    sold_product = SoldProduct.objects.create(item=product,
                                                              count=quantity,
                                                              user=user,
                                                              price=item.get('total_price'))
                    item_total_price = item.get('total_price')
                    user.profile.update_balance(-item_total_price, -bonus_use)
                    correct_total_price += item_total_price

                    # Удаление товара из корзины
                    cart.remove(product)
                logger.info(f'Заказ на сумму {correct_total_price} успешно оформлен')

                return HttpResponse(_('The goods have been successfully paid for'))
        return render(request, 'app_cart/cart.html', {'cart': cart, 'form': form})

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = CartAddProductForm(request.POST)
        pk = request.POST.get('edit_quantity')
        product = get_object_or_404(SellItem, id=pk)
        if form.is_valid():
            cd = form.cleaned_data
            cd['update'] = True
            cart.add(product=product,
                     quantity=cd['quantity'],
                     update_quantity=cd['update'])
        return redirect('cart_detail')



