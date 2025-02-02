from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import check_password
from django.db import transaction as dbt

from .models import *
from .serializers import *

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from datetime import datetime
from django.utils.dateparse import parse_datetime
from decimal import Decimal
import json

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# General Functions
def get_user_by_cpf(cpf):
    try:
        user = Users.objects.get(cpf=cpf)
    except:
        user = None
    return user

def get_account_by_acc_number(acc_number):
    try:
        account = Accounts.objects.get(account_number = acc_number)
    except:
        account = None
    return account

def validate_user(user):
    if user == None:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    if user.is_active == False:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_410_GONE)

def validate_self_user(request, user):
    validation = validate_user(user)
    if validation != None:
        return validation
    if user != request.user:
        return Response({"error": "Permissão negada."}, status=status.HTTP_403_FORBIDDEN)

def validate_admin_user(request, user):
    validation = validate_user(user)
    if validation != None:
        return validation
    if (user != request.user) and (not request.user.is_staff):
        return Response({"error": "Permissão negada."}, status=status.HTTP_403_FORBIDDEN)

def validate_account(account):
    if account == None:
        return Response({"error": "Conta não encontrada."}, status=status.HTTP_404_NOT_FOUND)
    if account.is_active == False:
        return Response({"error": "Conta não encontrada."}, status=status.HTTP_410_GONE)

# Verificar essa validação
def validate_self_user_account(user, account):
    validation = validate_account(account)
    if validation != None:
        return validation
    if account.account_user != user:
        Response({"error": "Usuário não pode acessar a conta."}, status=status.HTTP_400_BAD_REQUEST)


# Admin Permission Requests
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):

    if request.method == 'GET':
        users = Users.objects.filter(is_active = True)
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_user(request):

    if request.method == 'POST':
        data = request.data

        serializer = CreateUsersSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()

            return_data = UsersSerializer(user).data
            return Response(return_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user(request, cpf):

    if request.method == 'PUT':
        user = get_user_by_cpf(cpf)
        
        validation = validate_user(user)
        if validation != None:
            return validation

        data = request.data

        for field in ["username", "first_name", "last_name", "email", "cpf"]:
            if ( (data.get(field) != "") and (data[field] != getattr(user, field))):
                    setattr(user, field, data[field])
        
        if ( (data.get("password") != "") and (check_password(data["password"], user.password))):
                user.set_password(data["password"])
        
        user.save()

        return Response(UsersSerializer(user).data, status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, cpf):

    if request.method == 'DELETE':
        user  = get_user_by_cpf(cpf)
        
        validation = validate_user(user)
        if validation != None:
            return validation

        user.is_active = False
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def activate_user(request, cpf):

    if request.method == 'PUT':
        user = get_user_by_cpf(cpf)
        
        if user == None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.save()

        return Response(UsersSerializer(user).data ,status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_accounts(request):

    if request.method == 'GET':
        accounts = Accounts.objects.all()

        serializer = AccountsSerializer(accounts, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_transactions(request):

    if request.method == 'GET':
        transactions = Transactions.objects.all()

        serializer = TransactionsSerializer(transactions, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def make_deposit(request, cpf, account_number):

    if request.method == 'PUT':
        
        user = get_user_by_cpf(cpf)
    
        validation = validate_user(user)
        if validation != None:
            return validation
        
        account = get_account_by_acc_number(account_number)

        validation = validate_self_user_account(user, account)
        if validation != None:
            return validation
        
        data = request.data
        value = Decimal(data['value'])

        try: 
            with dbt.atomic():
                serializer = CreateTransactionsSerializer(data={'transaction_type': str(data['type']),
                                                                'transaction_value': value,
                                                                'transaction_source': account.id,
                                                                'transaction_destination': account.id})

                if serializer.is_valid():
                    transaction = serializer.save()
                else:
                    Response({'error': 'Problenas na criação da transação.'}, status=status.HTTP_400_BAD_REQUEST)
                
                account.account_balance += value
                account.save()
                
                return Response(TransactionsSerializer(transaction).data, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Saque não concluído. Erro inesperado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_400_BAD_REQUEST)

# Any Authenticated User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_self(request, cpf):

    if request.method == 'GET':
        user = get_user_by_cpf(cpf)

        validation = validate_self_user(request, user)
        if validation != None:
            return validation
        
        serializer = UserAccountsSerializer(user)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_self_account(request, cpf, account_number):

    if request.method == 'GET':
        
        user = get_user_by_cpf(cpf)
    
        validation = validate_self_user(request, user)
        if validation != None:
            return validation
        
        account = get_account_by_acc_number(account_number)

        validation = validate_self_user_account(user, account)
        if validation != None:
            return validation
        
        serializer = UserAccountSerializer(user, context={'account': account})
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_withdraw(request, cpf, account_number):

    if request.method == 'POST':

        user = get_user_by_cpf(cpf)
    
        validate_self_user(request, user)

        account = get_account_by_acc_number(account_number)

        validate_self_user_account(user, account)

        data = request.data
        value = Decimal(data['value'])

        if value > account.account_balance:
            return Response({"error": "Saldo Insuficiente."}, status=status.HTTP_400_BAD_REQUEST)
        

        try: 
            with dbt.atomic():
                serializer = CreateTransactionsSerializer(data={'transaction_type': str(data['type']),
                                                                'transaction_value': value,
                                                                'transaction_source': account.id,
                                                                'transaction_destination': account.id})

                if serializer.is_valid():
                    transaction = serializer.save()
                else:
                    Response({'error': 'Problenas na criação da transação.'}, status=status.HTTP_400_BAD_REQUEST)
                
                account.account_balance -= value
                account.save()
                
                return Response(TransactionsSerializer(transaction).data, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Saque não concluído. Erro inesperado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_transfer(request, cpf, account_number):

    if request.method == 'POST':
        
        user = get_user_by_cpf(cpf)
    
        validation = validate_self_user(request, user)
        if validation != None:
            return validation
        
        account = get_account_by_acc_number(account_number)

        validation = validate_self_user_account(user, account)
        if validation != None:
            return validation
        
        data = request.data
        value = Decimal(data['value'])

        if account.account_balance < value:
            return Response({"error": "Saldo insuficiente."}, status=status.HTTP_400_BAD_REQUEST)

        account_destination = get_account_by_acc_number(data['account_number'])
        validation = validate_account(account_destination)
        if validation != None:
            return validation
        
        try: 
            with dbt.atomic():
                serializer = CreateTransactionsSerializer(data={'transaction_type': str(data['type']),
                                                                'transaction_value': value,
                                                                'transaction_source': account.id,
                                                                'transaction_destination': account_destination.id})

                if serializer.is_valid():
                    transaction = serializer.save()
                else:
                    Response({'error': 'Problenas na criação da transação.'}, status=status.HTTP_400_BAD_REQUEST)
                
                account.account_balance -= value
                account_destination.account_balance += value
                account.save()
                account_destination.save()
                
                return Response(TransactionsSerializer(transaction).data, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Saque não concluído. Erro inesperado.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request, cpf, account_number):
    if request.method == 'GET':

        user = get_user_by_cpf(cpf)
    
        validation = validate_self_user(request, user)
        if validation != None:
            return validation
        
        account = get_account_by_acc_number(account_number)

        validation = validate_self_user_account(user, account)
        if validation != None:
            return validation

        transactions = Transactions.objects.filter(
            models.Q(transaction_source__account_number=account_number) | 
            models.Q(transaction_destination__account_number=account_number)
        ).select_related(
            'transaction_source__account_user',
            'transaction_destination__account_user'
        ).order_by('-transaction_date')

        date_str = request.query_params.get('date', None)
        
        if date_str:
            try:
                transaction_date = parse_datetime(date_str)
                if transaction_date:
                    transactions = transactions.filter(transaction_date__date=transaction_date.date())
                else:
                    return Response({"error": "Formado de data inválida (YYYY-MM-DD)."}, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({"error": "Formado de data inválida (YYYY-MM-DD)."}, status=status.HTTP_400_BAD_REQUEST)

        transactions = transactions.order_by('-transaction_date')

        serializer = HistoryTransactionsSerializer(transactions, many=True)

        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)