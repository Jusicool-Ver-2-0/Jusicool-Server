import random

from django.conf import settings
from django.contrib.auth import login
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from account.models import Account
from user.enums import UserStatus
from user.exceptions import CodeIsNotValidException, UserAlreadyExistException
from user.models import User
from user.serializers import EmailValidateSerializer, EmailRequestSerializer
from user.tasks import send_email


class EmailService:
    def __init__(
        self,
        user: User = User,
        account: Account = Account,
    ):
        self.user = user
        self.account = account

    @transaction.atomic
    def request(self, serializer: EmailRequestSerializer) -> None:
        email = serializer.validated_data.get("email")

        if self.user.objects.filter(email=email).exists():
            raise UserAlreadyExistException()

        self.user.objects.create(email=email)

        send_email.delay(email)

    @transaction.atomic
    def validate(self, request: Request, serializer: EmailValidateSerializer) -> None:
        email = serializer.validated_data.get("email")

        code = cache.get(email)
        if code != serializer.validated_data.get("code"):
            raise CodeIsNotValidException()

        user: User = get_object_or_404(self.user, email=email)
        user.status = UserStatus.ACTIVE
        user.save()

        cache.delete(email)
