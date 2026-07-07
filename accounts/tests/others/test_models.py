id="az6nqj"
import pytest

from accounts.models import User, Profile


@pytest.fixture
def user():
    return User.objects.create_user(
        phone="09123456789",
        email="test@example.com",
        first_name="Ali",
        last_name="Ahmadi",
        password="12345678",
    )


@pytest.fixture
def profile(user):
    return Profile.objects.create(
        user=user,
        bio="Test bio",
        address="Tehran",
    )


# ==========================================================
# User Model Tests
# ==========================================================

@pytest.mark.django_db
def test_user_str(user):
    assert str(user) == user.phone


@pytest.mark.django_db
def test_user_full_name(user):
    assert user.full_name == "Ali Ahmadi"


@pytest.mark.django_db
def test_user_default_flags(user):
    assert user.phone_verified is False
    assert user.email_verified is False
    assert user.is_admin is False
    assert user.is_staff is False


@pytest.mark.django_db
def test_user_username_field():
    assert User.USERNAME_FIELD == "phone"


@pytest.mark.django_db
def test_user_required_fields():
    assert User.REQUIRED_FIELDS == [
        "email",
        "first_name",
        "last_name",
    ]


# ==========================================================
# Profile Model Tests
# ==========================================================

@pytest.mark.django_db
def test_profile_str(profile, user):
    assert str(profile) == user.phone


@pytest.mark.django_db
def test_profile_user_relation(profile, user):
    assert profile.user == user
    assert user.profile == profile


@pytest.mark.django_db
def test_profile_optional_fields(profile):
    assert profile.bio == "Test bio"
    assert profile.address == "Tehran"


@pytest.mark.django_db
def test_profile_can_be_created_with_empty_fields(user):
    profile = Profile.objects.create(user=user)

    assert profile.bio is None
    assert profile.address is None
    assert profile.birth_date is None

