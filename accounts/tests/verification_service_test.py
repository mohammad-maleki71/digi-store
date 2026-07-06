id="zl7t3r"
import pytest
from unittest.mock import patch

from rest_framework.exceptions import ValidationError

from accounts.services.verification_service import VerificationService


@pytest.fixture
def registration_data():
    return {
        "phone": "09123456789",
        "email": "test@example.com",
        "first_name": "Ali",
        "last_name": "Ahmadi",
        "password": "hashed-password",
        "otp": "123456",
        "phone_verified": False,
        "email_verified": False,
    }


# ==========================================================
# verify_email Tests
# ==========================================================

@pytest.mark.django_db
@patch("accounts.services.verification_service.cache")
@patch.object(VerificationService, "create_user_if_verified")
def test_verify_email_success(
    mock_create_user,
    mock_cache,
    registration_data,
    settings,
):
    token = "token123"

    mock_cache.get.return_value = registration_data.copy()

    VerificationService.verify_email(token)

    saved_data = mock_cache.set.call_args.args[1]

    assert saved_data["email_verified"] is True

    mock_cache.set.assert_called_once_with(
        f"register:{token}",
        saved_data,
        timeout=settings.REGISTRATION_CACHE_TIMEOUT,
    )

    mock_create_user.assert_called_once()


@pytest.mark.django_db
@patch("accounts.services.verification_service.cache")
def test_verify_email_invalid_token(mock_cache):
    mock_cache.get.return_value = None

    with pytest.raises(ValidationError):
        VerificationService.verify_email("invalid-token")


# ==========================================================
# verify_phone Tests
# ==========================================================

@pytest.mark.django_db
@patch("accounts.services.verification_service.cache")
@patch.object(VerificationService, "create_user_if_verified")
def test_verify_phone_success(
    mock_create_user,
    mock_cache,
    registration_data,
    settings,
):
    token = "token123"

    mock_cache.get.return_value = registration_data.copy()

    VerificationService.verify_phone(
        token,
        "123456",
    )

    saved_data = mock_cache.set.call_args.args[1]

    assert saved_data["phone_verified"] is True

    mock_cache.set.assert_called_once_with(
        f"register:{token}",
        saved_data,
        timeout=settings.REGISTRATION_CACHE_TIMEOUT,
    )

    mock_create_user.assert_called_once()


@pytest.mark.django_db
@patch("accounts.services.verification_service.cache")
def test_verify_phone_invalid_token(mock_cache):
    mock_cache.get.return_value = None

    with pytest.raises(ValidationError):
        VerificationService.verify_phone(
            "invalid-token",
            "123456",
        )


@pytest.mark.django_db
@patch("accounts.services.verification_service.cache")
def test_verify_phone_invalid_otp(
    mock_cache,
    registration_data,
):
    mock_cache.get.return_value = registration_data

    with pytest.raises(ValidationError):
        VerificationService.verify_phone(
            "token123",
            "999999",
        )


# ==========================================================
# create_user_if_verified Tests
# ==========================================================

@pytest.mark.django_db
@patch("accounts.services.verification_service.cache.delete")
@patch("accounts.services.verification_service.logger.info")
def test_create_user_if_verified_success(
    mock_logger,
    mock_cache_delete,
):
    data = {
        "phone": "09123456789",
        "email": "test@example.com",
        "first_name": "Ali",
        "last_name": "Ahmadi",
        "password": "hashed-password",
        "phone_verified": True,
        "email_verified": True,
    }

    VerificationService.create_user_if_verified(
        "token123",
        data,
    )

    from accounts.models import User

    user = User.objects.get(phone="09123456789")

    assert user.email == "test@example.com"
    assert user.phone_verified is True
    assert user.email_verified is True
    assert user.is_active is True

    mock_logger.assert_called_once_with(
        "User %s registered successfully.",
        user.id,
    )

    mock_cache_delete.assert_called_once_with(
        "register:token123"
    )


@pytest.mark.django_db
@patch("accounts.services.verification_service.cache.delete")
def test_create_user_not_created_if_email_not_verified(
    mock_cache_delete,
):
    data = {
        "phone": "09123456789",
        "email": "test@example.com",
        "first_name": "Ali",
        "last_name": "Ahmadi",
        "password": "hashed-password",
        "phone_verified": True,
        "email_verified": False,
    }

    VerificationService.create_user_if_verified(
        "token123",
        data,
    )

    from accounts.models import User

    assert User.objects.count() == 0
    mock_cache_delete.assert_not_called()


@pytest.mark.django_db
@patch("accounts.services.verification_service.cache.delete")
def test_create_user_not_created_if_phone_not_verified(
    mock_cache_delete,
):
    data = {
        "phone": "09123456789",
        "email": "test@example.com",
        "first_name": "Ali",
        "last_name": "Ahmadi",
        "password": "hashed-password",
        "phone_verified": False,
        "email_verified": True,
    }

    VerificationService.create_user_if_verified(
        "token123",
        data,
    )

    from accounts.models import User

    assert User.objects.count() == 0
    mock_cache_delete.assert_not_called()
