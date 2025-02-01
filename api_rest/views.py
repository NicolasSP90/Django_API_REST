from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.hashers import check_password

from .models import *
from .serializers import *

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

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
        return Response(status=status.HTTP_404_NOT_FOUND)

    if user.is_active == False:
        return Response(status=status.HTTP_410_GONE)

def validate_self_user(request, user):
    validate_user(user)
    
    if user != request.user:
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

def validate_self_user_account(user, account):
    if account == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if account.account_user != user:
        Response(status=status.HTTP_400_BAD_REQUEST)


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
        user  = get_user_by_cpf(cpf)
        
        validate_user()

        data = request.data

        # Atualiza apenas campos não vazios
        for field in ["username", "first_name", "last_name", "email", "cpf"]:
            if ( (data.get(field) != "") and (data[field] != getattr(user, field))):
                    setattr(user, field, data[field])
        
        # Atualiza a senha apenas se diferente da atual
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
        
        validate_user()

        user.is_active = False
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def activate_user(request, cpf):

    if request.method == 'PUT':
        user  = get_user_by_cpf(cpf)
        
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


# Any Authenticated User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_self(request, cpf):

    if request.method == 'GET':
        user  = get_user_by_cpf(cpf)
        
        validate_self_user(request, user)
        
        serializer = UserAccountsSerializer(user)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_self_account(request, cpf, account_number):

    if request.method == 'GET':
        
        user = get_user_by_cpf(cpf)
    
        validate_self_user(request, user)
        
        account = get_account_by_acc_number(account_number)

        validate_self_user_account(user, account)
        
        serializer = UserAccountSerializer(user, context={'account': account})
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def make_withdraw(request, cpf, account_number):

    if request.method == 'PUT':

        user = get_user_by_cpf(cpf)
    
        validate_self_user(request, user)

        account = get_account_by_acc_number(account_number)

        validate_self_user_account(user, account)

        data = request.data

        value = Decimal(data['value'])
        print(value)
        print(account.account_balance)

        if value > account.account_balance:
            return Response({"error": "Saldo Insuficiente."}, status=status.HTTP_400_BAD_REQUEST)
        
        account.account_balance -= value
        account.save()

        return Response({"sucess": "Operação realizada com sucesso."}, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
