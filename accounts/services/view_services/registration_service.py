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
            data = validated_data.copy()

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

            send_email_task.delay(
                data["email"],
                verification_link
            )

            return verify_token
