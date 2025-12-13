from unittest.mock import MagicMock, patch

import pytest

from apps.users.factories import UserFactory
from apps.users.services import UserVerificationService


@pytest.mark.django_db
class TestUserVerificationService:

    @pytest.fixture(autouse=True)
    def mock_exist_user(self) -> UserFactory:
        return UserFactory.build(
            email="exist@test.com",
            is_active=True,
        )

    @patch("apps.users.services.send_email_verify_code.delay")
    def test_send_verification_code(
        self,
        mock_task,
    ):
        """메일 전송 task를 호출한다."""

        # Action
        UserVerificationService().send_verification_code(email="new@test.com")

        # Assert
        mock_task.assert_called_once_with(email="new@test.com")
