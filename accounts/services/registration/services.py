from django.core.mail import send_mail
from django.conf import settings


class EmailService:

    @staticmethod
    def send_verification_email(email, verification_link):

        send_mail(
            subject="Verify your email",
            message=f"Click the following link:\n\n{verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )


class SMSService:

    @staticmethod
    def send_verification_code(phone, code):

        if settings.SMS_BACKEND == "console":
            print("=" * 50)
            print(f"SMS To : {phone}")
            print(f"Verification Code : {code}")
            print("=" * 50)


