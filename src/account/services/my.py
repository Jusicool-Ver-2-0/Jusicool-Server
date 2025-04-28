from django.db import transaction

from account.models import Account


class MyAccountService:
    def __init__(self, account: Account = Account):
        self.account = account

    @transaction.atomic
    def get_my_account(self, user) -> Account:
        return self.account.objects.get(user=user)