"""Tests for communication tasks."""

from unittest.mock import MagicMock, patch

from core.communication.tasks import send_email


class TestSendEmail:
    """범용 이메일 전송 태스크 테스트"""

    @patch("core.communication.tasks.EmailMultiAlternatives")
    @patch("core.communication.tasks.render_to_string")
    def test_send_email(
        self,
        mock_render_to_string,
        mock_email_class,
    ):
        """이메일이 올바르게 전송되는지 확인"""
        # Arrange
        recipient = "test@example.com"
        subject = "Test Subject"
        template_name = "test_template.html"
        context = {"key": "value"}
        mock_html_content = "<html>Test</html>"
        mock_render_to_string.return_value = mock_html_content
        mock_email_instance = MagicMock()
        mock_email_class.return_value = mock_email_instance

        # Act
        send_email(
            recipient_email=recipient,
            subject=subject,
            template_name=template_name,
            context=context,
        )

        # Assert
        mock_render_to_string.assert_called_once_with(
            template_name=template_name,
            context=context,
        )
        mock_email_class.assert_called_once()
        call_kwargs = mock_email_class.call_args.kwargs
        assert call_kwargs["subject"] == subject
        assert call_kwargs["body"] == mock_html_content
        assert call_kwargs["to"] == [recipient]
        
        mock_email_instance.attach_alternative.assert_called_once_with(
            mock_html_content,
            "text/html",
        )
        mock_email_instance.send.assert_called_once()
