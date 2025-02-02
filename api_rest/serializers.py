from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

from .models import *

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['cpf'] = user.cpf
        return token

    def validate(self, attrs):
        # Mapear 'cpf' para o campo de autenticação esperado
        cpf = attrs.get('cpf')
        password = attrs.get('password')

        if not cpf or not password:
            raise serializers.ValidationError({"detail": "CPF e senha são necessários."})

        user = authenticate(username=cpf, password=password)

        if user is None:
            print("Autenticação falhou.")
        else:
            print(f"Usuário autenticado: {user}")

        if user is None:
            raise serializers.ValidationError({"detail": "Credenciais inválidas."})
        
        attrs['user'] = user

        return super().validate(attrs)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'email']


class CreateUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'email', 'cpf', 'password']
    
    def create(self, validated_data):
        user = Users(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_number', 'account_type', 'account_balance']


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ["account_number", "account_type"]


class UserAccountsSerializer(serializers.ModelSerializer):
    accounts = AccountSerializer(many=True, read_only=True)

    class Meta:
        model = Users
        fields = ["username", "first_name", "last_name", "cpf", "accounts"]


class UserAccountSerializer(serializers.ModelSerializer):
    account = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ["username", "first_name", "last_name", "cpf", "account"]
    
    def get_account(self, obj):
        account = self.context.get('account')
        if account:
            return AccountsSerializer(account).data


class CreateTransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["transaction_type", "transaction_value", "transaction_destination", "transaction_source"]