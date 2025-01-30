from rest_framework import serializers
from .models import Users, Accounts, Transactions

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'email', 'cpf']


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_number', 'account_type', 'account_balance']


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'