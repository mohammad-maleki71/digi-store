import pytest
from unittest.mock import patch

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="testuser",
        password="StrongPassword123"
    )


@pytest.mark.django_db
@patch("accounts.views.RefreshToken.for_user")
@patch("accounts.views.LoginSerializer")
@patch("accounts.views.logger.info")
def test_login_success(
    mock_logger,
    mock_serializer,
    mock_refresh,
    client,
    user,
):
    serializer = mock_serializer.return_value
    serializer.is_valid.return_value = True
    serializer.validated_data = {"user": user}

    refresh = mock_refresh.return_value
    refresh.access_token = "access-token"

    response = client.post(
        "/api/login/",
        {
            "username": "testuser",
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.data == {
        "refresh": str(refresh),
        "access": "access-token",
    }

    mock_serializer.assert_called_once_with(
        data={
            "username": "testuser",
            "password": "StrongPassword123",
        }
    )

    serializer.is_valid.assert_called_once_with(
        raise_exception=True
    )

    mock_refresh.assert_called_once_with(user)

    mock_logger.assert_called_once_with(
        "User %s logged in successfully.",
        user.id,
    )


@pytest.mark.django_db
@patch("accounts.views.LoginSerializer")
def test_login_validation_error(mock_serializer, client):
    serializer = mock_serializer.return_value
    serializer.is_valid.side_effect = ValidationError(
        {"detail": "Invalid credentials."}
    )

    response = client.post(
        "/api/login/",
        {
            "username": "wrong",
            "password": "wrong",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
@patch("accounts.views.RefreshToken.for_user")
@patch("accounts.views.LoginSerializer")
def test_tokens_are_returned(
    mock_serializer,
    mock_refresh,
    client,
    user,
):
    serializer = mock_serializer.return_value
    serializer.is_valid.return_value = True
    serializer.validated_data = {"user": user}

    refresh = mock_refresh.return_value
    refresh.access_token = "access-token"

    response = client.post(
        "/api/login/",
        {
            "username": "testuser",
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert "refresh" in response.data
    assert "access" in response.data


@pytest.mark.django_db
@patch("accounts.views.RefreshToken.for_user")
@patch("accounts.views.LoginSerializer")
def test_refresh_token_created(
    mock_serializer,
    mock_refresh,
    client,
    user,
):
    serializer = mock_serializer.return_value
    serializer.is_valid.return_value = True
    serializer.validated_data = {"user": user}

    response = client.post(
        "/api/login/",
        {
            "username": "testuser",
            "password": "StrongPassword123",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    mock_refresh.assert_called_once_with(user)

