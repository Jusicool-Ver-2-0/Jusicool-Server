from django.contrib.auth import login
from django.db import transaction
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from user.exceptions import UserAlreadyExistException
from user.models import User
from user.serializers import SignupSerializer, SigninSerializer


class AccountService:
    def __init__(self, user: User = User):
        self.user = user

    @transaction.atomic
    def signup(self, serializer: SignupSerializer) -> None:
        exists_user: bool = self.user.objects.filter(
            Q(email=serializer.validated_data.get("email"))
            | Q(username=serializer.validated_data.get("username"))
        ).exists()
        if exists_user:
            raise UserAlreadyExistException()

        serializer.save()

    @transaction.atomic
    def signin(self, request: Request, serializer: SigninSerializer) -> None:
        user = get_object_or_404(
            self.user,
            email=serializer.validated_data.get("email")
        )

        login(request=request, user=user)