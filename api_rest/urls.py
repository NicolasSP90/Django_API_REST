from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # Admin permissions ONLY
    # Check all Users
    path('users/', views.get_all_users, name='get_all_users'),
    
    # Users CRUD
    path('users/create_user/', views.create_user, name='create_user'),
    path('users/update_user/<str:cpf>/', views.update_user, name='update_user'),
    path('users/delete_user/<str:cpf>/', views.delete_user, name='delete_user'),
    path('users/activate_user/<str:cpf>/', views.activate_user, name='activate_user'),
    # path('user/<str:cpf>/account/<str:account_number>/deposit/', views.make_deposit, name='make_deposit') <- OBRIGATORIO

    # Check all Accounts
    path('accounts/', views.get_all_accounts, name='get_all_accounts'),
    
    # Accounts CRUD
    # path('accounts/create_account/', views.create_account, name=''),
    # path('accounts/update_account/<str:account_number>/', views.update_account, name=''),
    # path('accounts/delete_account/<str:account_number>/', views.delete_account, name=''),
    # path('accounts/activate_account/<str:account_number>/', views.activate_account, name=''),

    # Check all Transactions
    path('transactions/', views.get_all_transactions, name='get_all_transactions'),


    # Any Authenticated User
    # Own Information
    path('user/<str:cpf>/', views.get_self, name='get_self'),
    path('user/<str:cpf>/account/<str:account_number>/', views.get_self_account, name='get_self_account'),

    # Actions
    path('user/<str:cpf>/account/<str:account_number>/withdraw/', views.make_withdraw, name='make_withdraw'),
    path('user/<str:cpf>/account/<str:account_number>/transfer/', views.make_transfer, name='make_transfer'),
    # path('user/<str:cpf>/account/<str:account_number>/transfer/history', views.transaction_history, name='') <- OBRIGATORIO (COM FILTRO DE DATA)

    # Single User Search
    # path('users/user/<str:cpf>/', views.get_user_by_cpf, name=''), <- OBRIGATORIO

    # Single Account Search
    # path('accounts/account/<str:account_number>/', views.get_user_by_cpf, name=''), <- OBRIGATORIO


    
]