from django.core.management.base import BaseCommand
from api_rest.models import Users, Accounts, Transactions
import random

class Command(BaseCommand):
    help = "Popula o banco de dados com registros iniciais"
    def handle(self, *args, **kwargs):
        user_number = 100
        transactions_by_account = 10
        cpf_list = set()
        acc_list = set()

        while len(cpf_list) < user_number:
            cpf_list.add(random.randint(10000000000, 99999999999))
        cpf_list = list(cpf_list)

        while len(acc_list) < user_number:
            acc_list.add(random.randint(10000, 99999))
        acc_list = list(acc_list)

        accounts = []

        for i in range(user_number):
            user = Users.objects.create(
                password = f"User_{i}",
                username=f"User_{i}",
                first_name = f"User {i}",
                last_name = f"User {i}",
                email = f"user_{i}@example.com",
                cpf = cpf_list[i])
            
            user.set_password(f"User_{i}")
            user.save()
            
            acc = Accounts.objects.create(
                account_number = acc_list[i],
                account_type = random.choice(["CC", "CP"]),
                account_balance = random.uniform(100.0, 5000.0),
                account_user = user
            )

            accounts.append(acc)

        for acc in accounts:
            for _ in range(transactions_by_account):
                random_acc_number = random.choice([a for a in accounts if a != acc])
                random_type = random.choice(["DEPOSITO", "SAQUE", "TRANSFERENCIA", "PAGAMENTO"])

                def return_acc(acc_param, random_acc_number_param, acc_origin, acc_type):
                    if acc_origin == "source":
                        return acc_param
                    
                    else:
                        if (acc_type == "DEPOSITO") or (acc_type == "SAQUE"):
                            return acc_param
                        if (acc_type == "TRANSFERENCIA") or (acc_type == "PAGAMENTO"):
                            return random_acc_number_param

                Transactions.objects.create(
                    transaction_type = random_type,
                    transaction_value = random.uniform(100.0, 1000.0),
                    transaction_source = return_acc(acc, random_acc_number, "source", random_type),
                    transaction_destination = return_acc(acc, random_acc_number, "destination", random_type)
                )


        self.stdout.write(self.style.SUCCESS("Banco de dados populado com sucesso!"))