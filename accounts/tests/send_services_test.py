import pytest
from unittest.mock import patch

from django.conf import settings

from accounts.services import EmailService, SMSService


# ==========================================================
# EmailService Tests
# ==========================================================

@pytest.mark.django_db
@patch("accounts.services.send_mail")
def test_send_verification_email(mock_send_mail):
    email = "test@example.com"
    verification_link = "http://localhost:8000/verify/token123"

    EmailService.send_verification_email(
        email=email,
        verification_link=verification_link,
    )

    mock_send_mail.assert_called_once_with(
        subject="Verify your email",
        message=f"Click the following link:\n\n{verification_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


# ==========================================================
# SMSService Tests
# ==========================================================

@pytest.mark.django_db
@patch("builtins.print")
def test_send_verification_code_console_backend(mock_print, settings):
    settings.SMS_BACKEND = "console"

    phone = "09123456789"
    code = "123456"

    SMSService.send_verification_code(
        phone=phone,
        code=code,
    )

    assert mock_print.call_count == 4

    mock_print.assert_any_call("=" * 50)
    mock_print.assert_any_call(f"SMS To : {phone}")
    mock_print.assert_any_call(f"Verification Code : {code}")


@pytest.mark.django_db
@patch("builtins.print")
def test_send_verification_code_non_console_backend(mock_print, settings):
    settings.SMS_BACKEND = "kavenegar"

    SMSService.send_verification_code(
        phone="09123456789",
        code="123456",
    )

    mock_print.assert_not_called()
