from django.db import transaction
from django.shortcuts import get_object_or_404

from account.models import Account


class MyAccountService:
    def __init__(self, account: Account = Account):
        self.account = account

    @transaction.atomic
    def get_my_account(self, user) -> Account:
        return get_object_or_404(Account, user=user)
