from django.contrib.auth.models import User
from django.db import models, transaction
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
# Create your models here.


class ShopModel(models.Model):
    """ Модель магазина  """

    name = models.CharField(max_length=100, verbose_name=_('name'))
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('create at'))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('update at'))

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')


class SellItem(models.Model):
    """ Модель товара  """

    shop = models.ForeignKey(ShopModel, on_delete=models.CASCADE, related_name='sell_item')
    name = models.CharField(max_length=100, verbose_name=_('item name'))
    description = models.TextField(verbose_name=_('description'), blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'), default=Decimal('0.00'))
    number_count = models.PositiveIntegerField(verbose_name=_('number count'), default=0)

    class Meta:
        verbose_name = _('sell item')
        verbose_name_plural = _('sell items')

    def get_absolute_url(self):
        """ Метод абсолютного пути товара  """

        return reverse_lazy('item_detail', kwargs={'pk': self.id})


class SoldProduct(models.Model):
    """ Модель проданного продукта """

    item = models.ForeignKey(SellItem, on_delete=models.CASCADE, related_name='sold_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    count = models.PositiveIntegerField(verbose_name=_('count'), default=0)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name=_('create at'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'), default=Decimal('0.00'))

    class Meta:
        verbose_name = _('sold product')
        verbose_name_plural = _('sold products')
