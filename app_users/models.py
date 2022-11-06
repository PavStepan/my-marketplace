from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from app_shops.models import SellItem


class Profile(models.Model):
    """ Модель расширяющая модель User """

    status_choises = [
        ('b', _('Brose')),
        ('s', _('Silver')),
        ('g', _('Gold'))]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name=_('balance'))
    count_buy = models.PositiveIntegerField(default=0, verbose_name=_('count buy'))
    status = models.CharField(max_length=1, choices=status_choises, default='b')
    used_cash = models.PositiveIntegerField(default=0, verbose_name=_('used cash'))

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    @transaction.atomic
    def update_balance(self, balance):
        Profile.objects.filter(pk=self.pk).update(balance=self.balance+balance)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class BuyItem(models.Model):
    """ Модель товара купленного пользователем """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='buy_list')
    name = models.CharField(max_length=100, verbose_name=_('name'))
    number_count = models.PositiveIntegerField(verbose_name=_('number_count'), default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('price'), default=Decimal('0.00'))

    class Meta:
        verbose_name = _('item')
        verbose_name_plural = _('items')
