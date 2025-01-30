from django.shortcuts import render
from django.http import HttpRequest, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

import json


@api_view(['GET'])
def get_users(request):

    if request.method == 'GET':
        users = Users.objects.all()

        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_transactions(request):

    if request.method == 'GET':
        transactions = Transactions.objects.all()

        serializer = TransactionsSerializer(transactions, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_accounts(request):

    if request.method == 'GET':
        accounts = Accounts.objects.all()

        serializer = AccountsSerializer(accounts, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_by_username(request, username):

    try:
        user = Users.objects.get(username=username)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        
        serializer = UsersSerializer(user)

        return Response(serializer.data)

