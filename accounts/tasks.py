import logging
from celery import shared_task
from accounts.services.registration.send_services import SMSService
from accounts.services.registration.send_services import EmailService
from django.conf import settings

logger = logging.getLogger(__name__)


@shared_task
def send_sms_task(phone, code):

    try:
        logger.info(
            "Verification SMS sent to %s",
            phone
        )

        SMSService.send_verification_code(
            phone,
            code
        )
    except Exception :
        logger.exception(
            "Failed to send verification SMS to %s",
            phone
        )


@shared_task
def send_email_task(email, link):
    try:
        logger.info(
            "Verification email sent to %s",
            email
        )

        EmailService.send_verification_email(
            email,
            link
        )
    except Exception :
        logger.exception(
            "Failed to send verification email to %s",
            email
        )
