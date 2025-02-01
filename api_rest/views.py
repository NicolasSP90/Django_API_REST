from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

import json

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):

    if request.method == 'GET':
        users = Users.objects.all()
        serializer = UsersSerializer(users, many=True)
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


@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_accounts(request):

    if request.method == 'GET':
        accounts = Accounts.objects.all()

        serializer = AccountsSerializer(accounts, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_user(request):
    data = request.data

    serializer = CreateUsersSerializer(data=data)

    if serializer.is_valid():
        user = serializer.save()

        return_data = UsersSerializer(user).data
        return Response(return_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# Any Authenticated User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_by_cpf(request, cpf):
    try:
        user = Users.objects.get(cpf=cpf)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        
        serializer = UserAccountsSerializer(user)

        return Response(serializer.data)
