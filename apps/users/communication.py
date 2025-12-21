"""Email templates for user authentication."""

import random
from typing import Any

from core.cache.cache import Cache
from core.cache.prefix import CacheKeyPrefix
from core.communication.templates import EmailTemplate


class EmailVerificationTemplate(EmailTemplate):
    """이메일 인증 코드 발송 템플릿"""

    def __init__(self, email: str):
        self._email = email
        self._verification_code = self._generate_and_cache_code()

    def _generate_and_cache_code(self) -> int:
        """인증 코드 생성 및 캐시 저장"""
        code = random.randint(100000, 999999)
        Cache.set(
            prefix=CacheKeyPrefix.email_verification_code,
            key=self._email,
            value=code,
            timeout=60 * 10,
        )
        return code

    @property
    def recipient_email(self) -> str:
        """수신자 이메일"""
        return self._email

    def get_subject(self) -> str:
        """이메일 제목 반환"""
        return "Jusicool 메일 인증 코드"

    def get_template_name(self) -> str:
        """템플릿 파일명 반환"""
        return "verify_code.html"

    def get_context(self) -> dict[str, Any]:
        """템플릿 컨텍스트 반환"""
        return {
            "recipient_name": self._email,
            "verification_code": self._verification_code,
        }
