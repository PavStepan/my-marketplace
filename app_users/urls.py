from django.urls import path
from app_users.views import RegisterView, LoginUserView, LogoutUserView, ProfileView, BalanceReplenishmentView, \
    UpdateProfileView, BasketView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('profile/<int:pk>/balance_replenishment/', BalanceReplenishmentView.as_view(), name='balance_replenishment'),
    path('profile/<int:pk>/basket/', BasketView.as_view(), name='basket'),

]
