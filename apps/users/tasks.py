import random

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.cache.cache import Cache
from core.cache.prefix import CacheKeyPrefix


@shared_task
def send_verification_code(email: str) -> None:
    """인증 메일 전송"""

    code = random.randint(100000, 999999)

    Cache.set(
        prefix=CacheKeyPrefix.email_verification_code,
        key=email,
        value=code,
        timeout=60 * 10,
    )

    html_content = render_to_string(
        template_name="verify_code.html",
        context={
            "recipient_name": email,
            "verification_code": code,
        },
    )

    email_message = EmailMultiAlternatives(
        subject=f"Jusicool 메일 인증 코드",
        body=html_content,
        to=[email],
        from_email=settings.EMAIL_HOST_USER,
    )
    email_message.attach_alternative(
        html_content,
        "text/html",
    )
    email_message.send()
