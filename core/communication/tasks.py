"""Communication tasks for async email sending."""

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def send_email(
    recipient_email: str,
    subject: str,
    template_name: str,
    context: dict,
) -> None:
    """
    범용 이메일 전송 태스크
    
    Args:
        recipient_email: 수신자 이메일 주소
        subject: 이메일 제목
        template_name: 템플릿 파일명
        context: 템플릿 컨텍스트 데이터
    """
    html_content = render_to_string(
        template_name=template_name,
        context=context,
    )

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        to=[recipient_email],
        from_email=settings.EMAIL_HOST_USER,
    )
    email_message.attach_alternative(
        html_content,
        "text/html",
    )
    email_message.send()
