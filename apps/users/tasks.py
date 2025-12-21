from celery import shared_task

from apps.users.communication import EmailVerificationTemplate
from core.communication.tasks import send_email


@shared_task
def send_verification_code(email: str) -> None:
    """인증 메일 전송"""
    template = EmailVerificationTemplate(email=email)
    
    send_email.delay(
        recipient_email=template.recipient_email,
        subject=template.get_subject(),
        template_name=template.get_template_name(),
        context=template.get_context(),
    )
