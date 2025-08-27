from django.contrib.auth import authenticate, login
from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from account.models import Account
from user.enums import UserStatus
from user.exceptions import UserIsNotValidException, UserAlreadyExistException
from user.models import User
from user.serializers import SignupSerializer, SigninSerializer


class UserService:
    def __init__(self, user: User = User, account: Account = Account):
        self.user = user
        self.account = account

    @transaction.atomic
    def signup(self, serializer: SignupSerializer) -> None:
        exist_user: bool = self.user.objects.filter(
            username=serializer.validated_data.get("username")
        ).exists()
        if exist_user:
            raise UserAlreadyExistException()

        user = get_object_or_404(
            self.user, email=serializer.validated_data.get("email")
        )

        user.username = serializer.validated_data.get("username")
        user.set_password(serializer.validated_data.get("password"))
        user.school = serializer.validated_data.get("school")
        user.save()

        account = self.account.objects.create(user=user)

        account.krw_balance = 5000000
        account.save()

    @transaction.atomic
    def signin(self, request: Request, serializer: SigninSerializer) -> None:
        user: User = get_object_or_404(
            self.user, email=serializer.validated_data.get("email")
        )

        if user.status != UserStatus.ACTIVE:
            raise UserIsNotValidException()

        authenticated_user = authenticate(
            request,
            username=user.username,
            password=serializer.validated_data.get("password"),
        )
        if authenticated_user is None:
            raise UserIsNotValidException()

        login(request=request, user=authenticated_user)
