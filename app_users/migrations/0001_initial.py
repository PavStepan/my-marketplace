# Generated by Django 2.2 on 2022-11-05 17:07

from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, verbose_name='balance')),
                ('count_buy', models.PositiveIntegerField(default=0, verbose_name='count buy')),
                ('status', models.CharField(choices=[('b', 'Brose'), ('s', 'Silver'), ('g', 'Gold')], default='b', max_length=1)),
                ('used_cash', models.PositiveIntegerField(default=0, verbose_name='used cash')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'profile',
                'verbose_name_plural': 'profiles',
            },
        ),
        migrations.CreateModel(
            name='BuyItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('number_count', models.PositiveIntegerField(default=0, verbose_name='number_count')),
                ('price', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10, verbose_name='price')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buy_list', to='app_users.Profile')),
            ],
            options={
                'verbose_name': 'item',
                'verbose_name_plural': 'items',
            },
        ),
    ]
