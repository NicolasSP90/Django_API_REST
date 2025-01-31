from rest_framework import serializers
from .models import Users, Accounts, Transactions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


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
        fields = ['username', 'first_name', 'last_name', 'email', 'cpf']


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_number', 'account_type', 'account_balance']


class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'