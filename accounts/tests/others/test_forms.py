id="zjlwmk"
import pytest

from accounts.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)


# ==========================================================
# CustomUserCreationForm Tests
# ==========================================================

@pytest.mark.django_db
def test_creation_form_valid():
    form = CustomUserCreationForm(
        data={
            "phone": "09123456789",
            "email": "test@example.com",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_creation_form_password_mismatch():
    form = CustomUserCreationForm(
        data={
            "phone": "09123456789",
            "email": "test@example.com",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password1": "StrongPassword123",
            "password2": "WrongPassword",
        }
    )

    assert not form.is_valid()
    assert "Passwords do not match" in form.errors["__all__"]


@pytest.mark.django_db
def test_creation_form_save():
    form = CustomUserCreationForm(
        data={
            "phone": "09123456789",
            "email": "test@example.com",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        }
    )

    assert form.is_valid()

    user = form.save()

    assert user.phone == "09123456789"
    assert user.email == "test@example.com"
    assert user.check_password("StrongPassword123")


@pytest.mark.django_db
def test_creation_form_save_without_commit():
    form = CustomUserCreationForm(
        data={
            "phone": "09123456789",
            "email": "test@example.com",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password1": "StrongPassword123",
            "password2": "StrongPassword123",
        }
    )

    assert form.is_valid()

    user = form.save(commit=False)

    assert user.pk is None
    assert user.check_password("StrongPassword123")


# ==========================================================
# CustomUserChangeForm Tests
# ==========================================================

@pytest.mark.django_db
def test_change_form_initial(user):
    form = CustomUserChangeForm(instance=user)

    assert form.initial["phone"] == user.phone
    assert form.initial["email"] == user.email


@pytest.mark.django_db
def test_change_form_valid(user):
    form = CustomUserChangeForm(
        instance=user,
        data={
            "phone": user.phone,
            "email": user.email,
            "first_name": "Reza",
            "last_name": user.last_name,
            "password": user.password,
            "is_active": user.is_active,
            "is_staff": user.is_staff,
            "is_admin": user.is_admin,
            "is_superuser": user.is_superuser,
            "phone_verified": user.phone_verified,
            "email_verified": user.email_verified,
            "groups": [],
            "user_permissions": [],
        }
    )

    assert form.is_valid()
