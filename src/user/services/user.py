from django.contrib.auth import authenticate, login
from django.db import transaction
from django.db.models import Q
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from user.enums import UserStatus
from user.exceptions import UserIsNotValidException, UserAlreadyExistException
from user.models import User
from user.serializers import SignupSerializer, SigninSerializer


class UserService:
    def __init__(self, user: User = User):
        self.user= user

    @transaction.atomic
    def signup(self, serializer: SignupSerializer) -> None:
        exist_user: bool = self.user.objects.filter(
            Q(email=serializer.validated_data.get("email"))
            | Q(username=serializer.validated_data.get("username"))
        ).exists()
        if exist_user:
            raise UserAlreadyExistException()

        serializer.save()

    @transaction.atomic
    def signin(self, request: Request, serializer: SigninSerializer) -> None:
        user: User = get_object_or_404(
            self.user,
            email=serializer.validated_data.get("email")
        )

        if user.status != UserStatus.ACTIVE:
            raise UserIsNotValidException()

        authenticated_user = authenticate(
            request,
            username=serializer.validated_data.get("username"),
            password=serializer.validated_data.get("password")
        )
        login(request=request, user=authenticated_user)