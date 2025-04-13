import random

from django.conf import settings
from django.contrib.auth import login
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from accounts.exceptions import CodeIsNotValidException
from accounts.models import Account
from accounts.serializers import EmailValidateSerializer, EmailRequestSerializer


class EmailService:
    def __init__(self, account: Account = Account):
        self.account = account

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

        user: Account = get_object_or_404(
            self.account,
            email=serializer.validated_data.get("email")
        )
        user.status = Account.AccountStatus.ACTIVE
        user.save()

        cache.delete(serializer.validated_data.get("email"))

        login(request=request, user=user)