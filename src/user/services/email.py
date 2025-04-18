import random

from django.conf import settings
from django.contrib.auth import login
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from account.models import Account
from user.exceptions import CodeIsNotValidException
from user.models import User
from user.serializers import EmailValidateSerializer, EmailRequestSerializer


class EmailService:
    def __init__(
            self,
            user: User = User,
            account: Account = Account,
    ):
        self.user = user
        self.account = Account

    @transaction.atomic
    def request(self, serializer: EmailRequestSerializer) -> None:
        code = random.randint(100000, 999999)

        cache.set(
            serializer.validated_data.get("email"),
            code,
            timeout=60 * 5
        )

        EmailMessage(
            subject=f"Jusicool mail authentication",
            body=f'code: {code}',
            to=(serializer.validated_data.get("email"), ),
            from_email=settings.EMAIL_HOST_USER,
        ).send()

    @transaction.atomic
    def validate(self, request: Request, serializer: EmailValidateSerializer) -> None:
        code = cache.get(serializer.validated_data.get("email"))
        if code != serializer.validated_data.get("code"):
            raise CodeIsNotValidException()

        user: User = get_object_or_404(
            self.user,
            email=serializer.validated_data.get("email")
        )
        user.status = User.UserStatus.ACTIVE
        user.save()

        cache.delete(serializer.validated_data.get("email"))

        login(request=request, user=user)