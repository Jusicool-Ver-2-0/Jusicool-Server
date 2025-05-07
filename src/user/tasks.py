import logging
import random

from django.conf import settings
from django.core.cache import cache
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


@shared_task
def send_email(email_address):
    code = random.randint(100000, 999999)

    cache.set(
        email_address,
        code,
        timeout=60 * 5
    )

    context = {
        "recipient_name": email_address,
        "verification_code": code
    }

    html_content = render_to_string(
        "mail_template.html",
        context
    )

    email = EmailMultiAlternatives(
        subject=f"Jusicool mail authentication",
        body=html_content,
        to=(email_address,),
        from_email=settings.EMAIL_HOST_USER,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

    logger.info(f"Sending email to {email_address} code: {code} complete")