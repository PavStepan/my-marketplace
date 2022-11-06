from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView
from app_users.forms import RegisterForm, BalanceReplenishmentForm, UpdateProfileForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .permission.authenticatedpermissionsmixin import AuthenticatedUserPermissionsMixin, UserPermissionsMixin



class RegisterView(View):
    """ Класс представления регистрации """

    def get(self, request, *args, **kwargs):
        """ Метод получения get запроса формы регистрации """

        form = RegisterForm()
        return render(request, template_name='app_users/register.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        """ Метод получения post запроса с полями из формы регистрации """

        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        return render(request, template_name='app_users/register.html', context={'form': form})


class LoginUserView(LoginView):
    """ Класс формы login в приложении """

    template_name = 'app_users/login.html'


class LogoutUserView(LogoutView):
    """ Класс формы logout в приложении """

    next_page = '/'


class ProfileView(DetailView):
    """ Класс представления профиля пользователя """
    model = User
    template_name = 'app_users/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        page_user = get_object_or_404(User, id=self.kwargs['pk'])
        context['page_user'] = page_user
        return context


class UpdateProfileView(UserPermissionsMixin, UpdateView):

    model = User
    form_class = UpdateProfileForm
    template_name = 'app_users/update_profile.html'

    def get(self, request, *args, **kwargs):
        super(UpdateProfileView, self).get(request, *args, **kwargs)
        pk = kwargs.get('pk')
        form = self.form_class(instance=self.object)
        return self.render_to_response(context={'form': form, 'pk': pk})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        profile = self.get_object()
        form = self.form_class(request.POST, instance=profile, )
        if form.is_valid():
            form.save()
            return self.render_to_response(context={'form': form,
                                                    'pk': pk,
                                                    'msg': _('Changes saved successfully')})

        return self.render_to_response(context={'form': form, 'pk': pk})


class BalanceReplenishmentView(AuthenticatedUserPermissionsMixin, View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form_balance = BalanceReplenishmentForm
        return render(request,
                      template_name='app_users/balance_replenishment.html',
                       context={'form': form_balance, 'pk': pk})

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        form_balance = BalanceReplenishmentForm(request.POST)
        if form_balance.is_valid():
            form_balance.save(commit=False)
            balance = form_balance.cleaned_data['balance']
            if balance <= 0:
                msg = _('Invalid value')
            else:
                self.request.user.profile.update_balance(balance)
            return redirect(reverse_lazy('profile', kwargs={'pk': pk}))

        return render(request,
                      template_name='app_users/balance_replenishment.html',
                      context={'form': form_balance,
                               'pk': pk})


