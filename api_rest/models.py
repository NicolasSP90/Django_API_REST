from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    cpf = models.CharField(
        max_length=11, 
        unique=True, 
        default="")
    
    USERNAME_FIELD = 'cpf'

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

    account_balance = models.DecimalField(
        default=0.0, 
        decimal_places=2,
        max_digits=12)
    
    account_user = models.ForeignKey(
        Users, 
        on_delete=models.CASCADE, 
        related_name="accounts")
    
    def __str__(self):
        return f"{self.id} - Account {self.account_number} - Balance: {self.acc_balance}"


class Transactions(models.Model):    
    class TransactionType(models.TextChoices):
        DEPOSITO = "DEPOSITO", "Depósito"
        SAQUE = "SAQUE", "Saque"
        TRANSFERENCIA = "TRANSFERENCIA", "Transferência"
        PAGAMENTO = "PAGAMENTO", "Pagamento"

    transaction_type = models.CharField(
        choices=TransactionType.choices, 
        max_length=20)
    
    transaction_value = models.DecimalField(
        default=0.0, 
        decimal_places=2,
        max_digits=12)
    
    transaction_date = models.DateTimeField(auto_now_add=True)
    
    accounts = models.ManyToManyField(
        Accounts, 
        through='AccountsTransactions', 
        related_name='transactions')
    

class AccountsTransactions(models.Model):
    account = models.ForeignKey(
        Accounts, 
        on_delete=models.CASCADE)
    
    transaction = models.ForeignKey(
        Transactions, 
        on_delete=models.CASCADE)
    
    role = models.CharField(
        max_length=10, 
        choices=[('origem', 'Origem'), ('destino', 'Destino')])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['account', 'transaction'], 
                name='unique_account_transaction')
        ]
