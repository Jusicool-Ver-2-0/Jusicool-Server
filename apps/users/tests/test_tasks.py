from unittest.mock import patch

from apps.users.tasks import send_verification_code
from core.cache.prefix import CacheKeyPrefix


class TestSendVerificationCode:

    @patch("apps.users.communication.Cache.set")
    @patch("apps.users.communication.random.randint")
    @patch("core.communication.tasks.send_email.delay")
    def test_send_verification_code(
        self,
        mock_send_email,
        mock_randint,
        mock_cache_set,
    ):
        """인증 코드를 생성하고 캐시에 저장한 후 이메일을 전송한다."""

        # Arrange
        user_email = "test@example.com"
        mock_code = 123456
        mock_randint.return_value = mock_code

        # Action
        send_verification_code(email=user_email)

        # Assert
        mock_cache_set.assert_called_once_with(
            prefix=CacheKeyPrefix.email_verification_code,
            key=user_email,
            value=mock_code,
            timeout=600,
        )
        
        # Verify send_email was called with correct parameters
        mock_send_email.assert_called_once()
        call_kwargs = mock_send_email.call_args.kwargs
        assert call_kwargs["recipient_email"] == user_email
        assert call_kwargs["subject"] == "Jusicool 메일 인증 코드"
        assert call_kwargs["template_name"] == "verify_code.html"
        assert call_kwargs["context"]["recipient_name"] == user_email
        assert call_kwargs["context"]["verification_code"] == mock_code
