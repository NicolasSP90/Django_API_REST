from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

from .models import *

# JWT Customization
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['cpf'] = user.cpf
        return token

    def validate(self, attrs):
        cpf = attrs.get('cpf')
        password = attrs.get('password')

        if not cpf or not password:
            raise serializers.ValidationError({'error': 'CPF e senha são necessários.'})

        user = authenticate(username=cpf, password=password)

        if user is None:
            print('Autenticação falhou.')
        else:
            print(f'Usuário autenticado: {user}')

        if user is None:
            raise serializers.ValidationError({'error': 'Credenciais inválidas.'})
        
        attrs['user'] = user

        return super().validate(attrs)


# User Creation
class CreateUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'email', 'cpf', 'password']
    
    def create(self, validated_data):
        user = Users(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


# User Information
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'email']


# Account Creation
class CreateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_number', 'account_type', 'account_balance', 'account_user']


# Account Information
class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_number', 'account_type', 'account_balance']


# Transaction Information
class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'


# User Accounts Information (User)
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_number', 'account_type']


# User Accounts Information (Complete)
class UserAccountsSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'cpf', 'accounts']


# Information About User Account
class UserAccountSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'cpf', 'account']
    
    def get_account(self, obj):
        account = self.context.get('account')
        if account:
            return AccountsSerializer(account).data


# Transaction Creation
class CreateTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ['transaction_type', 'transaction_value', 'transaction_destination', 'transaction_source']


# Transaction History Serializers
class HistoryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username']

class HistoryAccountSerializer(serializers.ModelSerializer):
    account_user = HistoryUserSerializer(read_only=True)
    class Meta:
        model = Accounts
        fields = ['account_number', 'account_user']

class HistoryTransactionsSerializer(serializers.ModelSerializer):
    transaction_source = HistoryAccountSerializer(read_only=True)
    transaction_destination = HistoryAccountSerializer(read_only=True)

    class Meta:
        model = Transactions
        fields = [
            'id', 
            'transaction_type', 
            'transaction_value', 
            'transaction_date', 
            'transaction_source', 
            'transaction_destination'
        ]

