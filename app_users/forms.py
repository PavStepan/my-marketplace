from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import Profile


class RegisterForm(UserCreationForm):
    """ Класс формы регистрации пользователя """

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )


class UpdateProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


class BalanceReplenishmentForm(forms.ModelForm):
    """ Класс формы пополнения баланса """

    class Meta:
        model = Profile
        fields = ('balance', )
