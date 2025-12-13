import logging

from django.db import transaction

from apps.users.models import User
from apps.users.tasks import send_email_verify_code


class UserVerificationService:

    @transaction.atomic
    def send_verification_code(self, email: str) -> None:
        User.objects.get_or_create(
            email=email,
            defaults={"is_active": False},
        )

        send_email_verify_code.delay(email=email)
