id="lwzv1d"
import pytest

from accounts.models import User, Profile


@pytest.mark.django_db
def test_profile_created_after_user_creation():
    user = User.objects.create_user(
        phone="09123456789",
        email="test@example.com",
        first_name="Ali",
        last_name="Ahmadi",
        password="12345678",
    )

    assert Profile.objects.filter(user=user).exists()

    profile = Profile.objects.get(user=user)

    assert profile.user == user


@pytest.mark.django_db
def test_profile_not_created_again_on_user_update():
    user = User.objects.create_user(
        phone="09123456789",
        email="test@example.com",
        first_name="Ali",
        last_name="Ahmadi",
        password="12345678",
    )

    assert Profile.objects.count() == 1

    user.first_name = "Reza"
    user.save()

    assert Profile.objects.count() == 1
    assert Profile.objects.get(user=user)
