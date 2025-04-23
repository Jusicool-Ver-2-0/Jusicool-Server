import random

from django.conf import settings
from django.contrib.auth import login
from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request

from user.enums import UserStatus
from user.exceptions import CodeIsNotValidException
from user.models import User
from user.serializers import EmailValidateSerializer, EmailRequestSerializer


class EmailService:
    def __init__(self, user: User = User):
        self.user = user

    @transaction.atomic
    def request(self, serializer: EmailRequestSerializer) -> None:
        code = random.randint(100000, 999999)

        cache.set(
            serializer.validated_data.get("email"),
            code,
            timeout=60 * 5
        )

        context = {
            "recipient_name": serializer.validated_data.get("email"),
            "verification_code": code
        }

        html_content = render_to_string(
            "../templates/mail_template.html",
            context
        )

        email = EmailMultiAlternatives(
            subject=f"Jusicool mail authentication",
            body=html_content,
            to=(serializer.validated_data.get("email"), ),
            from_email=settings.EMAIL_HOST_USER,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

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

        cache.delete(serializer.validated_data.get("email"))

        login(request=request, user=user)