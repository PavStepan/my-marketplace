from django.contrib import admin
from app_users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """ Класс для отображения в админ панели модели профиля"""

    list_display = ['id', 'balance']


admin.site.register(Profile, ProfileAdmin)


