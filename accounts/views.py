import logging
from django.core.cache import cache
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.tasks import send_sms_task, send_email_task
from accounts.serializers import UserRegisterSerializer
from accounts.services.registration.registration import RegistrationService
from .services.registration.verification import VerificationService
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
    inline_serializer,
)
from rest_framework import serializers


logger = logging.getLogger(__name__)


@extend_schema(
    tags=["Authentication"],
    auth=[],

    operation_id="user_register",

    summary="User Registration",

    description="""
                    Registers a new user and sends a one-time verification code (OTP)
                    to the provided phone number or email.
                    A verification token is returned and must be used to complete 
                    the verification process before the account becomes active.
                """,

    request=UserRegisterSerializer,

    responses={
        201: inline_serializer(
            name="RegisterResponse",
            fields={
                "message": serializers.CharField(),
                "verify_token": serializers.UUIDField(),
            },
        ),

        400: OpenApiResponse(
            response=inline_serializer(
                name="ValidationError",
                fields={
                    "phone": serializers.ListField(
                        child=serializers.CharField(),
                        required=False
                    ),
                    "email": serializers.ListField(
                        child=serializers.CharField(),
                        required=False
                    ),
                }
            ),
            description="Validation error."
        )
    },

    examples=[
        OpenApiExample(
            "request example",
            request_only=True,
            value={
                "phone": "09123456789",
                "email": "m@gmail.com",
                "first_name": "mohammad",
                "last_name": "maleki",
                "password": "12345678",
                "confirm_password": "12345678",
            },
        ),

        OpenApiExample(
            "successfully created user account",
            response_only=True,
            status_codes=["201"],
            value={
                "message": "OTP sent successfully.",
                "verify_token": "d4b49766-cb5e-4ef2-8e54-ae9cb94b6ab0"
            },
        ),
    ],
)

class UserRegisterAPIView(APIView):

    def post(self, request):

        logger.info("User registration started.")

        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verify_token = RegistrationService.register(
            serializer.validated_data
        )

        logger.info("User registration completed successfully.")

        return Response(
            {
                "message": "OTP code and email, sent successfully.",
                "verify_token": verify_token
            },
            status=status.HTTP_201_CREATED
        )


@extend_schema(
    summary="Verify email",
    description="Verify user's email using the verification token.",
    parameters=[
        OpenApiParameter(
            name="token",
            type=str,
            location=OpenApiParameter.QUERY,
            required=True,
            description="Email verification token.",
        ),
    ],
    responses={
        200: OpenApiResponse(
            response={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "Email verified.",
                    }
                },
            },
            description="Email verified successfully.",
        ),
        400: OpenApiResponse(description="Invalid or expired token."),
    },
    tags=["Authentication"],
    auth=[],
)
class EmailVerificationAPIView(APIView):

    def get(self, request):

        token = request.query_params.get("token")

        VerificationService.verify_email(token)

        return Response({
            "message": "Email verified."
        })


@extend_schema(
    summary="Verify phone",
    description="Verify user's phone number using the verification token and OTP code.",
    request=inline_serializer(
        name="PhoneVerificationRequest",
        fields={
            "token": serializers.CharField(),
            "code": serializers.CharField(),
        },
    ),
    responses={
        200: inline_serializer(
            name="PhoneVerificationResponse",
            fields={
                "message": serializers.CharField(
                    default="Phone verified."
                ),
            },
        ),
        400: OpenApiResponse(description="Invalid or expired token/code."),
    },
    tags=["Authentication"],
    auth=[],
)
class PhoneVerificationAPIView(APIView):

    def post(self, request):

        token = request.data.get("token")
        code = request.data.get("code")

        VerificationService.verify_phone(
            token,
            code
        )

        return Response({
            "message": "Phone verified."
        })