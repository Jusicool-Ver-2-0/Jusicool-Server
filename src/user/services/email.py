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
from user.exceptions import CodeIsNotValidException
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
        send_email.delay(serializer.validated_data.get("email"))

    @transaction.atomic
    def validate(self, request: Request, serializer: EmailValidateSerializer) -> None:
        code = cache.get(serializer.validated_data.get("email"))
        if code != serializer.validated_data.get("code"):
            raise CodeIsNotValidException()

        user: User = get_object_or_404(
            self.user,
            email=serializer.validated_data.get("email")
        )
        user.status = UserStatus.ACTIVE
        user.save()

        self.account.objects.create(user=user)

        cache.delete(serializer.validated_data.get("email"))

        login(request=request, user=user)