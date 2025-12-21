"""Tests for user communication templates."""

from unittest.mock import patch

from apps.users.communication import EmailVerificationTemplate
from core.cache.prefix import CacheKeyPrefix


class TestEmailVerificationTemplate:
    """이메일 인증 템플릿 테스트"""

    @patch("apps.users.communication.Cache.set")
    @patch("apps.users.communication.random.randint")
    def test_email_verification_template(
        self,
        mock_randint,
        mock_cache_set,
    ):
        """이메일 인증 템플릿이 올바르게 생성되는지 확인"""
        # Arrange
        email = "test@example.com"
        mock_code = 123456
        mock_randint.return_value = mock_code

        # Act
        template = EmailVerificationTemplate(email=email)

        # Assert - 캐시 저장 확인
        mock_cache_set.assert_called_once_with(
            prefix=CacheKeyPrefix.email_verification_code,
            key=email,
            value=mock_code,
            timeout=600,
        )

        # Assert - 템플릿 속성 확인
        assert template.recipient_email == email
        assert template.get_subject() == "Jusicool 메일 인증 코드"
        assert template.get_template_name() == "verify_code.html"
        
        context = template.get_context()
        assert context["recipient_name"] == email
        assert context["verification_code"] == mock_code
