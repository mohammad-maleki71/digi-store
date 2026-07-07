import uuid
import pytest
from unittest.mock import patch
from rest_framework import status


@pytest.mark.django_db
@patch("accounts.views.RegistrationService.register")
def test_register_success(mock_register, api_client):

    verify_token = uuid.uuid4().hex

    mock_register.return_value = verify_token

    data = {
        "phone": "09123456789",
        "email": "test@gmail.com",
        "first_name": "Mohammad",
        "last_name": "Maleki",
        "password": "12345678",
        "confirm_password": "12345678",
    }

    response = api_client.post(
        "/api/accounts/register/",
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED

    assert response.data == {
        "message": "OTP code and email, sent successfully.",
        "verify_token": verify_token,
    }

    mock_register.assert_called_once()

    validated_data = mock_register.call_args.args[0]

    assert validated_data["phone"] == data["phone"]
    assert validated_data["email"] == data["email"]

@pytest.mark.django_db
def test_register_passwords_not_match(api_client):

    data = {
        "phone": "09123456789",
        "email": "test@gmail.com",
        "first_name": "Mohammad",
        "last_name": "Maleki",
        "password": "12345678",
        "confirm_password": "87654321",
    }

    response = api_client.post(
        "/api/accounts/register/",
        data,
        format="json",
    )

    assert response.status_code == 400

@pytest.mark.django_db
def test_register_without_phone(api_client):

    data = {
        "email": "test@gmail.com",
        "first_name": "Mohammad",
        "last_name": "Maleki",
        "password": "12345678",
        "confirm_password": "12345678",
    }

    response = api_client.post(
        "/api/accounts/register/",
        data,
        format="json",
    )

    assert response.status_code == 400
