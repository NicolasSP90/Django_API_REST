from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class Users(AbstractUser):
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        default="")
    
    password = models.CharField(
        max_length=255
    )
    
    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['username', 'email']

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True
    )

    def __str__(self):
        return f"{self.id} - {self.username} | {self.email}"


class Accounts(models.Model):
    account_number = models.IntegerField(default=0)

    class AccountType(models.TextChoices):
        CC = "CC", "Conta Corrente"
        CP = "CP", "Conta Poupança"

    account_type = models.CharField(
        choices=AccountType.choices, 
        max_length=20)

    account_balance = models.DecimalField(
        default=0.0, 
        decimal_places=2,
        max_digits=12)
    
    account_user = models.ForeignKey(
        Users, 
        on_delete=models.CASCADE, 
        related_name="accounts")
    
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id} - Account {self.account_number} - Balance: {self.account_balance}"


class Transactions(models.Model):    
    class TransactionType(models.TextChoices):
        DEPOSITO = "DEPOSITO", "Depósito"
        SAQUE = "SAQUE", "Saque"
        TRANSFERENCIA = "TRANSFERENCIA", "Transferência"

    transaction_type = models.CharField(
        choices=TransactionType.choices, 
        max_length=20)
    
    transaction_value = models.DecimalField(
        default=0.0, 
        decimal_places=2,
        max_digits=12)
    
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    transaction_source = models.ForeignKey(
        Accounts, 
        on_delete=models.CASCADE, 
        related_name='transaction_source'
    )
    transaction_destination = models.ForeignKey(
        Accounts, 
        on_delete=models.CASCADE, 
        related_name='transaction_destination'
    )
