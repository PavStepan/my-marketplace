from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from app_cart.forms import CartAddProductForm
from app_shops.models import ShopModel, SellItem, SoldProduct


class Menu(View):
    """ Класс для представления главной страницы приложения """

    def get(self, request, *args, **kwargs):
        return render(request, template_name='menu/menu.html')


class ListShop(ListView):
    """ Класс для представления списка магазинов"""

    model = ShopModel
    template_name = 'app_shops/list_shop.html'
    context_object_name = 'shop_list'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        shop_list = self.object_list.only('name').all()
        paginator = Paginator(shop_list, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = self.get_context_data()
        context['shop_list'] = page_obj
        return self.render_to_response(context)


class DetailItem(FormMixin, DetailView):
    """ Класс детального представления товара """

    model = SellItem
    template_name = 'app_shops/detail_item.html'
    context_object_name = 'item'
    form_class = CartAddProductForm


class StatisticView(ListView):
    """ Класс представления статистики продажи товара """

    model = SoldProduct
    context_object_name = 'item_list'
    template_name = 'app_shops/statistic.html'

    def get(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()
        context = self.get_context_data()

        item_list = self.object_list.select_related('item', 'user').all()

        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        print(date_to == '')
        if date_from:
            date_from = datetime.strptime(date_from, "%Y-%m-%d")
        if date_to:
            date_to = datetime.strptime(date_to, "%Y-%m-%d")

        if date_from != '' and date_to != '':
            if date_from == date_to:
                item_list = self.object_list.filter(create_at=date_from)
            elif date_from < date_to:
                item_list = self.object_list.filter(create_at__gte=date_from, create_at__lte=date_to)
            else:
                context['msg'] = _('date error')
        elif date_from and date_to == '':
            item_list = self.object_list.only('create_at').filter(create_at__gte=date_from)

        elif date_from == '' and date_to:
            item_list = self.object_list.only('create_at').filter(create_at__lte=date_to)
        else:
            context['msg'] = _('date error')

        total_cash = item_list.aggregate(total_cash=Sum('price'))
        paginator = Paginator(item_list, 25)
        page_number = request.GET.get('page')
        item_list = paginator.get_page(page_number)

        context['item_list'] = item_list
        context['total_cash'] = total_cash
        return self.render_to_response(context)
