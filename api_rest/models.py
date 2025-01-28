from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=150, default="")
    user_cpf = models.CharField(max_length=11, unique=True, default="")
    user_email = models.EmailField(unique=True, default="")
    user_password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_id} - {self.user_name} | {self.user_email}"

class Accounts(models.Model):
    acc_number = models.IntegerField(primary_key=True)
    acc_balance = models.FloatField(default=0.0)
    acc_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="accounts")


class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    acc_base = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.TextChoices("transaction_type", "DEPOSITO SAQUE TRANSFERENCIA PAGAMENTO")
    transaction = models.CharField(choices=transaction_type.choices)
    transaction_value = models.FloatField(default=0.0)
    transaction_date = models.DateTimeField(auto_now_add=True)