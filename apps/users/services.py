from django.db import transaction

from apps.users.models import User
from apps.users.tasks import send_verification_code


class EmailVerificationService:

    @transaction.atomic
    def send_verification_email(
        self,
        email: str,
    ) -> None:
        """인증 메일 발송"""

        User.objects.get_or_create(
            email=email,
        )

        send_verification_code.delay(email=email)
