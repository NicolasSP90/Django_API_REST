from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # Users CRUD - Admin permissions ONLY
    path('users/create_user/', views.create_user, name='create_user'), 
    path('users/update_user/<str:cpf>/', views.update_user, name='update_user'),
    path('users/delete_user/<str:cpf>/', views.delete_user, name='delete_user'),
    path('users/activate_user/<str:cpf>/', views.activate_user, name='activate_user'),

    # Accounts CRUD - Admin permissions ONLY
    path('accounts/create_account/<str:cpf>/', views.create_account, name='create_account'),
    path('accounts/delete_account/<str:account_number>/', views.delete_account, name='delete_account'),
    path('accounts/activate_account/<str:account_number>/', views.activate_account, name='activate_account'), 
    # Necessário que os demais retornos de contas levem em conta o activate

    # Search Actions
    path('users/', views.get_all_users, name='get_all_users'), # Admin permissions ONLY
    path('accounts/', views.get_all_accounts, name='get_all_accounts'), # Admin permissions ONLY
    path('transactions/', views.get_all_transactions, name='get_all_transactions'), # Admin permissions ONLY
    path('user/<str:cpf>/', views.get_self, name='get_self'), # Self User or Admin
    path('user/<str:cpf>/account/<str:account_number>/', views.get_self_account, name='get_self_account'), # Self User or Admin
    path('account/<str:account_number>/', views.get_account, name='get_account'), # Admin permissions ONLY

    # Actions
    path('user/<str:cpf>/account/<str:account_number>/deposit/', views.make_deposit, name='make_deposit'), # Admin Only
    path('user/<str:cpf>/account/<str:account_number>/withdraw/', views.make_withdraw, name='make_withdraw'), # Any Authenticated User (self Only)
    path('user/<str:cpf>/account/<str:account_number>/transfer/', views.make_transfer, name='make_transfer'), # Any Authenticated User (self Only)
    path('user/<str:cpf>/account/<str:account_number>/history/', views.transaction_history, name='transaction_history'), # Self User or Admin
]