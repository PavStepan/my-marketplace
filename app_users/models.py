from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
import logging


logger = logging.getLogger(__name__)


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
    bonus_points = models.PositiveIntegerField(default=0, verbose_name=_('bonus points'))

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    @transaction.atomic
    def update_balance(self, balance, bonus=0):
        profile = Profile.objects.get(pk=self.pk)

        if balance > 0:
            # Пополнение баланса
            profile.balance = self.balance + balance
            profile.save(update_fields=['balance'])

        else:
            # Списание с баланса и обработка бонусов

            if abs(balance) < abs(bonus):
                raise 'Некорректное значение бонусных баллов'
            balance -= bonus
            profile.balance = self.balance + balance

            if profile.status == 's':
                cash_back = 5
            elif profile.status == 'g':
                cash_back = 10
            else:
                cash_back = 3
            if profile.status is not None:
                profile.bonus_points += abs(balance / 100) * cash_back + bonus

            if bonus < 0:
                pass
                logger.info(f'Пользователь {profile.user} использовал {bonus} бонусов')

            profile.save(update_fields=['balance', 'bonus_points'])

            if profile.balance < 0:
                raise ValueError('Баланс счета не может быть отрицательным')
            if balance < 0:
                profile.used_cash = self.used_cash + abs(balance)
                profile.save(update_fields=['used_cash'])
                status_before = profile.status
                if 50000 < profile.used_cash < 100000:
                    profile.status = 's'
                elif profile.used_cash > 100000:
                    profile.status = 'g'
                profile.save(update_fields=['status'])
                if profile.status != status_before:
                    logger.info(f'Статус пользователя {get_object_or_404(User, self.pk)} изменен на {profile.status}')




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
