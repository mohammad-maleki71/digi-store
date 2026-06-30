import logging
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from accounts.models import User
from django.conf import settings

logger = logging.getLogger(__name__)


class VerificationService:

    @staticmethod
    def verify_email(token):
        data = cache.get(f"register:{token}")
        if not data:
            raise ValidationError(
                {"error": "Invalid or expired token."}
            )

        data["email_verified"] = True

        cache.set(
            f"register:{token}",
            data,
            timeout=settings.REGISTRATION_CACHE_TIMEOUT
        )

        VerificationService.create_user_if_verified(
            token,
            data
        )

    @staticmethod
    def verify_phone(token, code):

        data = cache.get(f"register:{token}")

        if not data:
            raise ValidationError(
                {"error": "Invalid or expired token."}
            )

        if data["otp"] != code:
            raise ValidationError(
                {"error": "Invalid OTP."}
            )

        data["phone_verified"] = True

        cache.set(
            f"register:{token}",
            data,
            timeout=settings.REGISTRATION_CACHE_TIMEOUT
        )

        VerificationService.create_user_if_verified(
            token,
            data
        )

    @staticmethod
    def create_user_if_verified(token, data):

        if not (
                data["phone_verified"] and
                data["email_verified"]
        ):
            return

        User.objects.create(
            phone=data["phone"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            password=data["password"],
            phone_verified=True,
            email_verified=True,
            is_active=True,
        )

        cache.delete(
            f"register:{token}"
        )