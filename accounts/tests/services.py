from unittest.mock import patch
from django.test import TestCase
from accounts.services import VerificationService


class VerificationServiceTest(TestCase):

    @patch("accounts.services.VerificationService.create_user_if_verified")
    @patch("accounts.services.cache.set")
    @patch("accounts.services.cache.get")
    def test_verify_email_success(
        self,
        mock_cache_get,
        mock_cache_set,
        mock_create_user,
    ):

        token = "token123"

        data = {
            "phone": "09123456789",
            "email": "ali@test.com",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password": "12345678",
            "email_verified": False,
            "phone_verified": False,
        }

        mock_cache_get.return_value = data

        VerificationService.verify_email(token)

        mock_cache_get.assert_called_once_with(
            "register:token123"
        )

        self.assertTrue(data["email_verified"])

        mock_cache_set.assert_called_once_with(
            "register:token123",
            data,
            timeout=settings.REGISTRATION_CACHE_TIMEOUT
        )

        mock_create_user.assert_called_once_with(
            token,
            data
        )

    @patch("accounts.services.VerificationService.create_user_if_verified")
    @patch("accounts.services.cache.set")
    @patch("accounts.services.cache.get")
    def test_verify_phone_success(
            self,
            mock_cache_get,
            mock_cache_set,
            mock_create_user,
    ):
        token = "token123"

        data = {
            "otp": "123456",
            "phone": "09123456789",
            "email": "ali@test.com",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password": "12345678",
            "phone_verified": False,
            "email_verified": False,
        }

        mock_cache_get.return_value = data

        VerificationService.verify_phone(
            token,
            "123456"
        )

        self.assertTrue(data["phone_verified"])

        mock_cache_set.assert_called_once_with(
            "register:token123",
            data,
            timeout=settings.REGISTRATION_CACHE_TIMEOUT
        )

        mock_create_user.assert_called_once_with(
            token,
            data
        )


    @patch("accounts.services.cache.delete")
    @patch("accounts.services.User.objects.create")
    def test_create_user_if_verified_success(
            self,
            mock_create,
            mock_cache_delete,
    ):
        data = {
            "phone": "09123456789",
            "email": "ali@test.com",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password": "12345678",
            "phone_verified": True,
            "email_verified": True,
        }

        VerificationService.create_user_if_verified(
            "token123",
            data
        )

        mock_create.assert_called_once_with(
            phone="09123456789",
            email="ali@test.com",
            first_name="Ali",
            last_name="Ahmadi",
            password="12345678",
            phone_verified=True,
            email_verified=True,
            is_active=True,
        )

        mock_cache_delete.assert_called_once_with(
            "register:token123"
        )