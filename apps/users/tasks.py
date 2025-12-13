import random

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.cache.cache import Cache
from core.cache.prefix import CacheKeyPrefix


@shared_task()
def send_email_verify_code(user_email: str) -> None:
    code = random.randint(100000, 999999)

    Cache.set(
        prefix=CacheKeyPrefix.email_verification_code,
        key=user_email,
        value=code,
        timeout=60 * 10,
    )

    html_content = render_to_string(
        template_name="verify_code.html",
        context={
            "recipient_name": user_email,
            "verification_code": code,
        },
    )

    email = EmailMultiAlternatives(
        subject=f"Jusicool 메일 인증 코드",
        body=html_content,
        to=[user_email],
        from_email=settings.EMAIL_HOST_USER,
    )
    email.attach_alternative(
        html_content,
        "text/html",
    )
    email.send()
