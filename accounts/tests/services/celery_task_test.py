id="n7p2va"
import pytest
from unittest.mock import patch

from accounts.tasks import (
    send_sms_task,
    send_email_task,
)


# ==========================================================
# send_sms_task Tests
# ==========================================================

@pytest.mark.django_db
@patch("accounts.tasks.logger.info")
@patch("accounts.tasks.SMSService.send_verification_code")
def test_send_sms_task_success(
    mock_send_sms,
    mock_logger,
):
    send_sms_task(
        "09123456789",
        "123456",
    )

    mock_logger.assert_called_once_with(
        "Verification SMS sent to %s",
        "09123456789",
    )

    mock_send_sms.assert_called_once_with(
        "09123456789",
        "123456",
    )


@pytest.mark.django_db
@patch("accounts.tasks.logger.exception")
@patch("accounts.tasks.SMSService.send_verification_code")
def test_send_sms_task_exception(
    mock_send_sms,
    mock_logger,
):
    mock_send_sms.side_effect = Exception("SMS Error")

    send_sms_task(
        "09123456789",
        "123456",
    )

    mock_logger.assert_called_once_with(
        "Failed to send verification SMS to %s",
        "09123456789",
    )


# ==========================================================
# send_email_task Tests
# ==========================================================

@pytest.mark.django_db
@patch("accounts.tasks.logger.info")
@patch("accounts.tasks.EmailService.send_verification_email")
def test_send_email_task_success(
    mock_send_email,
    mock_logger,
):
    send_email_task(
        "test@example.com",
        "http://localhost/verify",
    )

    mock_logger.assert_called_once_with(
        "Verification email sent to %s",
        "test@example.com",
    )

    mock_send_email.assert_called_once_with(
        "test@example.com",
        "http://localhost/verify",
    )


@pytest.mark.django_db
@patch("accounts.tasks.logger.exception")
@patch("accounts.tasks.EmailService.send_verification_email")
def test_send_email_task_exception(
    mock_send_email,
    mock_logger,
):
    mock_send_email.side_effect = Exception("Email Error")

    send_email_task(
        "test@example.com",
        "http://localhost/verify",
    )

    mock_logger.assert_called_once_with(
        "Failed to send verification email to %s",
        "test@example.com",
    )

