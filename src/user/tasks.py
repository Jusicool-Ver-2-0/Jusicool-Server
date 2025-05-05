import random

from django.conf import settings
from django.core.cache import cache
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_email(email):
    code = random.randint(100000, 999999)

    cache.set(
        email,
        code,
        timeout=60 * 5
    )

    context = {
        "recipient_name": email,
        "verification_code": code
    }

    html_content = render_to_string(
        "../templates/mail_template.html",
        context
    )

    email = EmailMultiAlternatives(
        subject=f"Jusicool mail authentication",
        body=html_content,
        to=(email,),
        from_email=settings.EMAIL_HOST_USER,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()