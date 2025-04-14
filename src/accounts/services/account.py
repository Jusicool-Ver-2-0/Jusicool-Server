from django.contrib.auth import login
from django.db import transaction
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from accounts.exceptions import AccountAlreadyExistException
from accounts.models import Account
from accounts.serializers import SignupSerializer, SigninSerializer


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

    @transaction.atomic
    def signin(self, request: Request, serializer: SigninSerializer) -> None:
        user = get_object_or_404(
            self.account,
            email=serializer.validated_data.get("email")
        )

        login(request=request, user=user)