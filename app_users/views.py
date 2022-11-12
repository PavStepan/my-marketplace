from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, UpdateView, ListView, FormView
from app_users.forms import RegisterForm, BalanceReplenishmentForm, UpdateProfileForm
from app_shops.models import SoldProduct
from django.utils.translation import gettext_lazy as _
from .permission.authenticatedpermissionsmixin import AuthenticatedUserPermissionsMixin, UserPermissionsMixin
from django.core.paginator import Paginator
from django.contrib.auth import login as auth_login
import logging

logger = logging.getLogger(__name__)


class RegisterView(View):
    """ Класс представления регистрации """

    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, template_name='app_users/register.html', context={'form': form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            logger.info(f'Аутентификация {user} прошла успешно')
            return redirect('/')
        return render(request, template_name='app_users/register.html', context={'form': form})


class LoginUserView(LoginView):
    """ Класс формы login в приложении """

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        logger.info(f'Аутентификация {form.get_user()} прошла успешно')
        return HttpResponseRedirect(self.get_success_url())

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
    """ Модель редактирования профиля """

    model = User
    form_class = UpdateProfileForm
    template_name = 'app_users/update_profile.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('update_profile', kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super(UpdateProfileView, self).get_context_data(**kwargs)
        context['msg'] = _('Changes saved successfully')
        return context


class BalanceReplenishmentView(AuthenticatedUserPermissionsMixin, FormView):
    """ Модель пополнения баланса """

    template_name = 'app_users/balance_replenishment.html'
    form_class = BalanceReplenishmentForm

    def get_success_url(self, **kwargs):
        pk = self.kwargs['pk']
        return reverse_lazy('balance_replenishment', kwargs={'pk': pk})

    def get_context_data(self, **kwargs):
        context = super(BalanceReplenishmentView, self).get_context_data(**kwargs)
        context['msg'] = _('The balance has been successfully replenished')
        return context

    def form_valid(self, form, *args, **kwargs):

        profile = form.save(commit=False)
        self.request.user.profile.update_balance(profile.balance)
        return super(BalanceReplenishmentView, self).form_valid(form)

    # def get(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     form_balance = BalanceReplenishmentForm
    #     return render(request,
    #                   template_name='app_users/balance_replenishment.html',
    #                    context={'form': form_balance, 'pk': pk})
    #
    # def post(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     form_balance = BalanceReplenishmentForm(request.POST)
    #     if form_balance.is_valid():
    #         form_balance.save(commit=False)
    #         balance = form_balance.cleaned_data['balance']
    #         if balance <= 0:
    #             msg = _('Invalid value')
    #         else:
    #             self.request.user.profile.update_balance(balance)
    #             logger.info(f'Баланс пользователя {request.user} пополнен на {balance}')
    #
    #         return redirect(reverse_lazy('profile', kwargs={'pk': pk}))
    #
    #     return render(request,
    #                   template_name='app_users/balance_replenishment.html',
    #                   context={'form': form_balance,
    #                            'pk': pk})


class HistoryView(ListView):
    """ Модель истории покупок """

    model = SoldProduct
    context_object_name = 'history_list'
    template_name = 'app_users/history.html'

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        history_list = self.object_list.select_related('item').filter(user=request.user)
        paginator = Paginator(history_list, 100)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = self.get_context_data()
        context['history_list'] = page_obj
        return self.render_to_response(context)
