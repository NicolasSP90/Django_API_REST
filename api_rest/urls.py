from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    # Admin permissions ONLY
    path('users/', views.get_all_users, name='get_all_users'),
    path('transactions/', views.get_all_transactions, name='get_all_transactions'),
    path('accounts/', views.get_all_accounts, name='get_all_accounts'),
    path('create_user/', views.create_user, name='create_user'),
    # path('update_user/', views.update_user, name='update_user'),
    # path('delete_user/', views.delete_user, name='delete_user'),
    

    # Any Authenticated User
    # path('user/<str:cpf>/', views.get_by_cpf, name='get_by_cpf'),
    # path('update_self_user/', views.update_self_user, name='update_self_user'),
    # path('delete_self_user/', views.delete_self_user, name='delete_self_user'),
    
]