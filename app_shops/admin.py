from django.contrib import admin
from app_shops.models import ShopModel, SellItem
# Register your models here.


class SellItemInTabular(admin.TabularInline):
    """ Класс для отображения в админ панели списка продаваемых товаров в виде таблицы"""
    model = SellItem


class ShopModelAdmin(admin.ModelAdmin):
    """ Класс для отображения в админ панели списка магазинов """

    list_display = ['id', 'name']
    inlines = [SellItemInTabular]


admin.site.register(ShopModel, ShopModelAdmin)
admin.site.register(SellItem)

