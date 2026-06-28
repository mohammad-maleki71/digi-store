from celery import shared_task
from accounts.services.registration.services import SMSService
from accounts.services.registration.services import EmailService


@shared_task
def send_sms_task(phone, code):

    SMSService.send_verification_code(
        phone,
        code
    )

@shared_task
def send_email_task(email, link):

    EmailService.send_verification_email(
        email,
        link
    )

