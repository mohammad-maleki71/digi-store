import pytest
from django.core.cache import cache
from django.contrib.auth.hashers import check_password
from unittest.mock import patch

from accounts.services.view_services.registration_service import (
    RegistrationService,
)


@pytest.mark.django_db
@patch(
    "accounts.services.registration.registration_service.send_email_task.delay"
)
@patch(
    "accounts.services.registration.registration_service.send_sms_task.delay"
)
def test_register_success(
    mock_sms,
    mock_email,
):

    validated_data = {
        "phone": "09123456789",
        "email": "test@gmail.com",
        "first_name": "Mohammad",
        "last_name": "Maleki",
        "password": "12345678",
        "password_confirm": "12345678",
    }

    verify_token = RegistrationService.register(validated_data)

    assert isinstance(verify_token, str)

    cached_data = cache.get(f"register:{verify_token}")

    assert cached_data is not None

    assert cached_data["phone"] == validated_data["phone"]
    assert cached_data["email"] == validated_data["email"]
    assert cached_data["first_name"] == validated_data["first_name"]
    assert cached_data["last_name"] == validated_data["last_name"]

    assert "password_confirm" not in cached_data

    assert check_password(
        validated_data["password"],
        cached_data["password"],
    )

    assert cached_data["phone_verified"] is False
    assert cached_data["email_verified"] is False

    assert "otp" in cached_data

    mock_sms.assert_called_once_with(
        validated_data["phone"],
        cached_data["otp"],
    )

    verification_link = (
        f"{settings.BACKEND_URL}"
        f"/api/accounts/verify-email/?token={verify_token}"
    )

    mock_email.assert_called_once_with(
        validated_data["email"],
        verification_link,
    )