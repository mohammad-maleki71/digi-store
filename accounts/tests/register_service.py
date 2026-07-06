id="ew1k0q"
import pytest
from unittest.mock import patch

from django.conf import settings

from accounts.services.registration_service import RegistrationService


@pytest.fixture
def validated_data():
    return {
        "phone": "09123456789",
        "email": "test@example.com",
        "first_name": "Ali",
        "last_name": "Ahmadi",
        "password": "12345678",
        "password_confirm": "12345678",
    }


# ==========================================================
# RegistrationService Tests
# ==========================================================

@pytest.mark.django_db
@patch("accounts.services.registration_service.send_email_task.delay")
@patch("accounts.services.registration_service.send_sms_task.delay")
@patch("accounts.services.registration_service.cache.set")
@patch("accounts.services.registration_service.uuid.uuid4")
@patch("accounts.services.registration_service.generate_otp")
@patch("accounts.services.registration_service.make_password")
def test_register_success(
    mock_make_password,
    mock_generate_otp,
    mock_uuid,
    mock_cache_set,
    mock_send_sms,
    mock_send_email,
    validated_data,
):
    mock_make_password.return_value = "hashed-password"
    mock_generate_otp.return_value = "123456"

    mock_uuid.return_value.hex = "verify-token"

    token = RegistrationService.register(validated_data)

    assert token == "verify-token"

    mock_make_password.assert_called_once_with("12345678")
    mock_generate_otp.assert_called_once()

    cached_data = {
        "phone": "09123456789",
        "email": "test@example.com",
        "first_name": "Ali",
        "last_name": "Ahmadi",
        "password": "hashed-password",
        "otp": "123456",
        "phone_verified": False,
        "email_verified": False,
    }

    mock_cache_set.assert_called_once_with(
        "register:verify-token",
        cached_data,
        timeout=settings.REGISTRATION_CACHE_TIMEOUT,
    )

    mock_send_sms.assert_called_once_with(
        "09123456789",
        "123456",
    )

    verification_link = (
        f"{settings.BACKEND_URL}"
        "/api/accounts/verify-email/?token=verify-token"
    )

    mock_send_email.assert_called_once_with(
        "test@example.com",
        verification_link,
    )


@pytest.mark.django_db
@patch("accounts.services.registration_service.send_email_task.delay")
@patch("accounts.services.registration_service.send_sms_task.delay")
@patch("accounts.services.registration_service.cache.set")
@patch("accounts.services.registration_service.uuid.uuid4")
@patch("accounts.services.registration_service.generate_otp")
@patch("accounts.services.registration_service.make_password")
def test_password_confirm_removed(
    mock_make_password,
    mock_generate_otp,
    mock_uuid,
    mock_cache_set,
    mock_send_sms,
    mock_send_email,
    validated_data,
):
    mock_make_password.return_value = "hashed-password"
    mock_generate_otp.return_value = "654321"
    mock_uuid.return_value.hex = "token123"

    RegistrationService.register(validated_data)

    cached_data = mock_cache_set.call_args.args[1]

    assert "password_confirm" not in cached_data


@pytest.mark.django_db
@patch("accounts.services.registration_service.send_email_task.delay")
@patch("accounts.services.registration_service.send_sms_task.delay")
@patch("accounts.services.registration_service.cache.set")
@patch("accounts.services.registration_service.uuid.uuid4")
@patch("accounts.services.registration_service.generate_otp")
@patch("accounts.services.registration_service.make_password")
def test_password_is_hashed(
    mock_make_password,
    mock_generate_otp,
    mock_uuid,
    mock_cache_set,
    mock_send_sms,
    mock_send_email,
    validated_data,
):
    mock_make_password.return_value = "hashed-password"
    mock_generate_otp.return_value = "123456"
    mock_uuid.return_value.hex = "token"

    RegistrationService.register(validated_data)

    cached_data = mock_cache_set.call_args.args[1]

    assert cached_data["password"] == "hashed-password"
    assert cached_data["password"] != "12345678"


@pytest.mark.django_db
@patch("accounts.services.registration_service.send_email_task.delay")
@patch("accounts.services.registration_service.send_sms_task.delay")
@patch("accounts.services.registration_service.cache.set")
@patch("accounts.services.registration_service.uuid.uuid4")
@patch("accounts.services.registration_service.generate_otp")
@patch("accounts.services.registration_service.make_password")
def test_verification_flags_are_false(
    mock_make_password,
    mock_generate_otp,
    mock_uuid,
    mock_cache_set,
    mock_send_sms,
    mock_send_email,
    validated_data,
):
    mock_make_password.return_value = "hashed-password"
    mock_generate_otp.return_value = "123456"
    mock_uuid.return_value.hex = "token"

    RegistrationService.register(validated_data)

    cached_data = mock_cache_set.call_args.args[1]

    assert cached_data["phone_verified"] is False
    assert cached_data["email_verified"] is False
