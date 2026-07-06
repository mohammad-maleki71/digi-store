from unittest.mock import patch
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class ProfileAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="12345678"
        )
        self.client.force_authenticate(self.user)
        self.url = reverse("profile")

    def test_get_profile(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("accounts.views.logger.info")
    def test_update_profile_logs(self, mock_logger):
        response = self.client.patch(
            self.url,
            {"bio": "hello"},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        mock_logger.assert_called_once_with(
            "Profile %s updated by user %s",
            self.user.profile.id,
            self.user.id,
        )