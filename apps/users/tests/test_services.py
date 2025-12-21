from unittest.mock import MagicMock, patch

import pytest

from apps.users.factories import UserFactory
from apps.users.services import EmailVerificationService


@pytest.mark.django_db
class TestEmailVerificationService:

    @pytest.fixture(autouse=True)
    def mock_exist_user(self) -> UserFactory:
        return UserFactory.build(
            email="exist@test.com",
            is_active=True,
        )

    @patch("apps.users.services.send_verification_code.delay")
    def test_send_verification_email(
        self,
        mock_task,
    ):
        """메일 전송 task를 호출한다."""

        # Action
        EmailVerificationService().send_verification_email(email="new@test.com")

        # Assert
        mock_task.assert_called_once_with(email="new@test.com")
