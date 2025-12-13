from unittest.mock import patch

from apps.users.tasks import send_email_verify_code
from core.cache.prefix import CacheKeyPrefix


class TestSendEmailVerifyCode:

    @patch("apps.users.tasks.Cache.set")
    @patch("apps.users.tasks.random.randint")
    def test_send_email_verify_code(
        self,
        mock_randint,
        mock_cache_set,
    ):
        """인증 코드를 생성하고 캐시에 저장한 후 이메일을 전송한다."""

        # Arrange
        user_email = "test@example.com"
        mock_code = 123456
        mock_randint.return_value = mock_code

        # Action
        send_email_verify_code(user_email=user_email)

        # Assert
        mock_cache_set.assert_called_once_with(
            prefix=CacheKeyPrefix.email_verification_code,
            key=user_email,
            value=mock_code,
            timeout=600,
        )
