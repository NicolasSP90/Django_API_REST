from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('users/', views.get_users, name='get_all_users'),
    path('transactions/', views.get_transactions, name='get_all_transactions'),
    path('accounts/', views.get_accounts, name='get_all_accounts'),
    path('user/<str:username>', views.get_by_username),
]