id="qzopm9"
import pytest

from accounts.models import User


# ==========================================================
# create_user Tests
# ==========================================================

@pytest.mark.django_db
def test_create_user_success():
    user = User.objects.create_user(
        phone="09123456789",
        email="test@example.com",
        first_name="Ali",
        last_name="Ahmadi",
        password="StrongPassword123",
    )

    assert user.phone == "09123456789"
    assert user.email == "test@example.com"
    assert user.first_name == "Ali"
    assert user.last_name == "Ahmadi"

    assert user.check_password("StrongPassword123")
    assert user.password != "StrongPassword123"

    assert user.is_active is False
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.is_admin is False


@pytest.mark.django_db
def test_create_user_without_phone():
    with pytest.raises(ValueError, match="Phone number is required"):
        User.objects.create_user(
            phone="",
            email="test@example.com",
            first_name="Ali",
            last_name="Ahmadi",
            password="12345678",
        )


@pytest.mark.django_db
def test_create_user_without_email():
    with pytest.raises(ValueError, match="Email is required"):
        User.objects.create_user(
            phone="09123456789",
            email="",
            first_name="Ali",
            last_name="Ahmadi",
            password="12345678",
        )


@pytest.mark.django_db
def test_create_user_without_password():
    with pytest.raises(ValueError, match="Password is required"):
        User.objects.create_user(
            phone="09123456789",
            email="test@example.com",
            first_name="Ali",
            last_name="Ahmadi",
            password=None,
        )


@pytest.mark.django_db
def test_email_is_normalized():
    user = User.objects.create_user(
        phone="09123456789",
        email="TEST@EXAMPLE.COM",
        first_name="Ali",
        last_name="Ahmadi",
        password="12345678",
    )

    assert user.email == "TEST@example.com"


# ==========================================================
# create_superuser Tests
# ==========================================================

@pytest.mark.django_db
def test_create_superuser_success():
    user = User.objects.create_superuser(
        phone="09111111111",
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        password="AdminPassword123",
    )

    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.is_admin is True
    assert user.is_active is True

    assert user.check_password("AdminPassword123")


@pytest.mark.django_db
def test_create_superuser_email_normalized():
    user = User.objects.create_superuser(
        phone="09111111111",
        email="ADMIN@EXAMPLE.COM",
        first_name="Admin",
        last_name="User",
        password="12345678",
    )

    assert user.email == "ADMIN@example.com"


@pytest.mark.django_db
def test_create_superuser_has_required_permissions():
    user = User.objects.create_superuser(
        phone="09111111111",
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        password="12345678",
    )

    assert user.is_admin
    assert user.is_staff
    assert user.is_superuser
    assert user.is_active

