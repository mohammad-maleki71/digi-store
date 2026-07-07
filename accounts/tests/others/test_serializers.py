import pytest

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import (
    UserRegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserSerializer,
    ProfileSerializer,
)
from accounts.models import Profile


@pytest.fixture
def user(django_user_model):
    user = django_user_model.objects.create_user(
        phone="09123456789",
        email="test@example.com",
        first_name="Ali",
        last_name="Ahmadi",
        password="12345678",
    )

    Profile.objects.create(
        user=user,
        bio="Test Bio",
        address="Tehran",
    )

    return user


# ==========================================================
# UserRegisterSerializer Tests
# ==========================================================

@pytest.mark.django_db
def test_register_serializer_valid_data():
    data = {
        "phone": "09111111111",
        "email": "user@test.com",
        "first_name": "Ali",
        "last_name": "Ahmadi",
        "password": "12345678",
        "password_confirm": "12345678",
    }

    serializer = UserRegisterSerializer(data=data)

    assert serializer.is_valid()


@pytest.mark.django_db
def test_register_serializer_password_mismatch():
    data = {
        "phone": "09111111111",
        "email": "user@test.com",
        "first_name": "Ali",
        "last_name": "Ahmadi",
        "password": "12345678",
        "password_confirm": "87654321",
    }

    serializer = UserRegisterSerializer(data=data)

    assert not serializer.is_valid()
    assert "password" in serializer.errors


# ==========================================================
# LoginSerializer Tests
# ==========================================================

@pytest.mark.django_db
def test_login_serializer_valid(user):
    serializer = LoginSerializer(
        data={
            "phone": user.phone,
            "password": "12345678",
        }
    )

    assert serializer.is_valid()
    assert serializer.validated_data["user"] == user


@pytest.mark.django_db
def test_login_serializer_invalid_password(user):
    serializer = LoginSerializer(
        data={
            "phone": user.phone,
            "password": "wrongpassword",
        }
    )

    assert not serializer.is_valid()


@pytest.mark.django_db
def test_login_serializer_invalid_phone():
    serializer = LoginSerializer(
        data={
            "phone": "09999999999",
            "password": "12345678",
        }
    )

    assert not serializer.is_valid()


# ==========================================================
# LogoutSerializer Tests
# ==========================================================

@pytest.mark.django_db
def test_logout_serializer_valid(user):
    refresh = RefreshToken.for_user(user)

    serializer = LogoutSerializer(
        data={
            "refresh": str(refresh)
        }
    )

    assert serializer.is_valid()

    # نباید Exception ایجاد کند
    serializer.save()


@pytest.mark.django_db
def test_logout_serializer_invalid_token():
    serializer = LogoutSerializer(
        data={
            "refresh": "invalid-token"
        }
    )

    assert serializer.is_valid()

    with pytest.raises(serializers.ValidationError):
        serializer.save()


# ==========================================================
# UserSerializer Tests
# ==========================================================

@pytest.mark.django_db
def test_user_serializer(user):
    serializer = UserSerializer(user)

    assert serializer.data["phone"] == user.phone
    assert serializer.data["email"] == user.email
    assert serializer.data["first_name"] == user.first_name
    assert serializer.data["last_name"] == user.last_name


# ==========================================================
# ProfileSerializer Tests
# ==========================================================

@pytest.mark.django_db
def test_profile_serializer(user):
    profile = user.profile

    serializer = ProfileSerializer(profile)

    assert serializer.data["bio"] == profile.bio
    assert serializer.data["address"] == profile.address
    assert serializer.data["user"]["phone"] == user.phone
    assert serializer.data["user"]["email"] == user.email
    assert serializer.data["user"]["first_name"] == user.first_name
    assert serializer.data["user"]["last_name"] == user.last_name
