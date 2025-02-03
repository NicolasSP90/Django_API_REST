from api_rest.models import *

from rest_framework.response import Response
from rest_framework import status

# Get User from CPF
def get_user_by_cpf(cpf):
    try:
        user = Users.objects.get(cpf=cpf)
    except:
        user = None
    return user


# Get Account by account_number
def get_account_by_acc_number(acc_number):
    try:
        account = Accounts.objects.get(account_number = acc_number)
    except:
        account = None
    return account


# User validation
def validate_user(user):
    if user == None:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
    if user.is_active == False:
        return Response({"error": "Usuário não encontrado."}, status=status.HTTP_410_GONE)


# Validate if user is the current session user
def validate_self_user(request, user):
    validation = validate_user(user)
    if validation != None:
        return validation
    if user != request.user:
        return Response({"error": "Permissão negada."}, status=status.HTTP_403_FORBIDDEN)


# Validate if the session user is admin
def validate_admin_user(request, user):
    validation = validate_user(user)
    if validation != None:
        return validation
    if (user != request.user) and (not request.user.is_staff):
        return Response({"error": "Permissão negada."}, status=status.HTTP_403_FORBIDDEN)

# Validate account
def validate_account(account):
    if account == None:
        return Response({"error": "Conta não encontrada."}, status=status.HTTP_404_NOT_FOUND)
    if account.is_active == False:
        return Response({"error": "Conta não encontrada."}, status=status.HTTP_410_GONE)

# Validate if the account is from the specified user
def validate_self_user_account(user, account):
    validation = validate_account(account)
    if validation != None:
        return validation
    if account.account_user != user:
        Response({"error": "Usuário não pode acessar a conta."}, status=status.HTTP_400_BAD_REQUEST)