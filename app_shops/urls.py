from django.urls import path
from app_shops.views import Menu, ListShop


urlpatterns = [
    path('', Menu.as_view(), name='menu'),
    path('shop_list/', ListShop.as_view(), name='shop_list'),

]