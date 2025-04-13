from django.db import transaction
from django.db.models import Q

from accounts.exceptions import AccountAlreadyExistException
from accounts.models import Account
from accounts.serializers import SignupSerializer


class AccountService:
    def __init__(self, account: Account = Account):
        self.account = account

    @transaction.atomic
    def signup(self, serializer: SignupSerializer) -> None:
        exist_account: bool = self.account.objects.filter(
            Q(email=serializer.validated_data.get("email"))
            | Q(username=serializer.validated_data.get("username"))
        ).exists()
        if exist_account:
            raise AccountAlreadyExistException()

        serializer.save()
