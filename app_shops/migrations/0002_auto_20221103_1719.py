# Generated by Django 3.2 on 2022-11-03 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_shops', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellitem',
            name='item_name',
            field=models.CharField(max_length=100, verbose_name='item name'),
        ),
        migrations.AlterField(
            model_name='sellitem',
            name='number_count',
            field=models.PositiveIntegerField(default=0, max_length=10, verbose_name='number count'),
        ),
        migrations.AlterField(
            model_name='sellitem',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to='app_shops.shopmodel'),
        ),
    ]
