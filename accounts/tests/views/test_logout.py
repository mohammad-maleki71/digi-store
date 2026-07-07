import pytest
from unittest.mock import patch

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from accounts.models import Profile


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser",
        password="StrongPassword123"
    )
    Profile.objects.create(user=user)
    return user


@pytest.mark.django_db
@patch("accounts.views.LogoutSerializer")
@patch("accounts.views.logger.info")
def test_logout_success(mock_logger, mock_serializer, client, user):
    client.force_authenticate(user=user)

    serializer = mock_serializer.return_value
    serializer.is_valid.return_value = True

    response = client.post(
        "/api/logout/",
        {},
        format="json",
        REMOTE_ADDR="127.0.0.1"
    )

    assert response.status_code == status.HTTP_205_RESET_CONTENT
    assert response.data == {
        "message": "Logout successful."
    }

    mock_serializer.assert_called_once_with(data={})
    serializer.is_valid.assert_called_once_with(raise_exception=True)
    serializer.save.assert_called_once()

    mock_logger.assert_called_once_with(
        "User %s logged out. IP: %s",
        user.id,
        "127.0.0.1"
    )


@pytest.mark.django_db
@patch("accounts.views.LogoutSerializer")
def test_logout_validation_error(mock_serializer, client, user):
    client.force_authenticate(user=user)

    serializer = mock_serializer.return_value
    serializer.is_valid.side_effect = ValidationError(
        {"refresh": ["Invalid token."]}
    )

    response = client.post(
        "/api/logout/",
        {},
        format="json"
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    serializer.is_valid.assert_called_once_with(
        raise_exception=True
    )
    serializer.save.assert_not_called()


@pytest.mark.django_db
def test_logout_requires_authentication(client):
    response = client.post(
        "/api/logout/",
        {},
        format="json"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
@patch("accounts.views.LogoutSerializer")
def test_serializer_save_called(mock_serializer, client, user):
    client.force_authenticate(user=user)

    serializer = mock_serializer.return_value
    serializer.is_valid.return_value = True

    response = client.post(
        "/api/logout/",
        {},
        format="json"
    )

    assert response.status_code == status.HTTP_205_RESET_CONTENT

    serializer.save.assert_called_once()


@pytest.mark.django_db
@patch("accounts.views.LogoutSerializer")
@patch("accounts.views.logger.info")
def test_logout_logs_user_and_ip(mock_logger, mock_serializer, client, user):
    client.force_authenticate(user=user)

    serializer = mock_serializer.return_value
    serializer.is_valid.return_value = True

    client.post(
        "/api/logout/",
        {},
        format="json",
        REMOTE_ADDR="192.168.1.10"
    )

    mock_logger.assert_called_once_with(
        "User %s logged out. IP: %s",
        user.id,
        "192.168.1.10"
    )

