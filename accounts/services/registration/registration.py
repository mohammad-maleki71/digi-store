import logging
import uuid
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from accounts.tasks import send_sms_task, send_email_task
from accounts.utils import generate_otp


logger = logging.getLogger(__name__)


class RegistrationService:

    @staticmethod
    def register(validated_data):
        try:
            data = validated_data.copy()

            logger.info(
                "User registration started for email=%s",
                data["email"],
            )

            data.pop("password_confirm")

            data["password"] = make_password(data["password"])

            data["otp"] = generate_otp()

            data["phone_verified"] = False
            data["email_verified"] = False

            verify_token = uuid.uuid4().hex

            cache.set(
                f"register:{verify_token}",
                data,
                timeout=settings.REGISTRATION_CACHE_TIMEOUT
            )

            verification_link = (
                f"{settings.BACKEND_URL}"
                f"/api/accounts/verify-email/?token={verify_token}"
            )

            send_sms_task.delay(
                data["phone"],
                data["otp"]
            )
            logger.info(
                "SMS verification task queued."
            )

            send_email_task.delay(
                data["email"],
                verification_link
            )
            logger.info(
                f"Email verification task queued. Link: {verification_link}"
            )

            logger.info(
                "User registration completed successfully."
            )

            return verify_token
        except Exception:
            logger.exception("User registration failed.")
            raise
