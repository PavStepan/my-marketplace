from django.contrib.auth import get_user_model
from django.db import transaction
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from app_cart.forms import CartAddProductForm
from app_shops.models import ShopModel, SellItem
from app_cart.cart import Cart


class Menu(View):
    """ Класс для представления главной страницы приложения """

    def get(self, request, *args, **kwargs):
        return render(request, template_name='menu/menu.html')


class ListShop(ListView):
    """ Класс для представления списка магазинов"""

    model = ShopModel
    template_name = 'app_shops/list_shop.html'
    context_object_name = 'shop_list'
    #
    # def get(self, request, *args, **kwargs):
    #     self.object_list = self.get_queryset()
    #     context = self.get_context_data()
    #     cart = Cart(request)
    #     buy_request = self.request.GET.get('Buy_button')
    #     print(self.request.GET)
    #     if buy_request:
    #         num_request = self.request.GET.get('num')
    #         if num_request:
    #             buy_count = num_request
    #         else:
    #             buy_count = 1
    #
    #         buy_request = buy_request.split(' ')
    #
    #
    #         command = buy_request[0]
    #         shop = buy_request[1]
    #         item = buy_request[2]
    #         if command == 'buy':
    #             if shop.startswith('shop') and item.startswith('item') and \
    #                     shop[4:].isdigit() and item[4:].isdigit():
    #
    #                 shop = get_object_or_404(self.object_list.only('id'), pk=shop[4:])
    #                 item = get_object_or_404(shop.sell_item, pk=item[4:])
    #
    #
    #             else:
    #                 context['msg'] = _('Product or store not found')
    #         else:
    #             context['msg'] = _('Unknown command')
    #     return self.render_to_response(context)


class DetailItem(FormMixin, DetailView):
    model = SellItem
    template_name = 'app_shops/detail_item.html'
    context_object_name = 'item'
    form_class = CartAddProductForm
