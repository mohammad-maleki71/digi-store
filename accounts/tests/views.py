from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserRegisterAPIViewTest(APITestCase):

    @patch("accounts.views.RegistrationService.register")
    def test_user_register_success(self, mock_register):

        mock_register.return_value = "token123"

        url = reverse("user-register")

        data = {
            "phone": "09123456789",
            "email": "ali@test.com",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password": "12345678",
            "password_confirm": "12345678"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            response.data["message"],
            "OTP code and email, sent successfully."
        )

        self.assertEqual(
            response.data["verify_token"],
            "token123"
        )

        mock_register.assert_called_once()

        mock_register.assert_called_once_with({
            "phone": "09123456789",
            "email": "ali@test.com",
            "first_name": "Ali",
            "last_name": "Ahmadi",
            "password": "12345678",
            "password_confirm": "12345678"
        })


class EmailVerificationAPIViewTest(APITestCase):

    @patch("accounts.views.VerificationService.verify_email")
    def test_verify_email_success(self, mock_verify_email):

        url = reverse("verify-email")

        response = self.client.get(
            url,
            {"token": "abc123"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data["message"],
            "Email verified."
        )

        mock_verify_email.assert_called_once()

        mock_verify_email.assert_called_once_with("abc123")


class PhoneVerificationAPIViewTest(APITestCase):

    @patch("accounts.views.VerificationService.verify_phone")
    def test_verify_phone_success(self, mock_verify_phone):

        url = reverse("verify-phone")

        data = {
            "token": "abc123",
            "code": "123456"
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.data["message"],
            "Phone verified."
        )

        mock_verify_phone.assert_called_once()

        mock_verify_phone.assert_called_once_with(
            "abc123",
            "123456"
        )