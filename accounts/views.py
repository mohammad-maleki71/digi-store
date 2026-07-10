import logging
from django.core.cache import cache
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.tasks import send_sms_task, send_email_task
from accounts.serializers import UserRegisterSerializer, ProfileSerializer, LoginSerializer, LogoutSerializer
from accounts.services.view_services.registration_service import RegistrationService
from accounts.services.view_services.verify_email_phone import VerificationService
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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
)


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

        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verify_token = RegistrationService.register(
            serializer.validated_data
        )

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

        logger.info(
            "email verified email successfully.",
        )

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

        logger.info(
            "phone verified phone successfully.",
        )

        return Response({
            "message": "Phone verified."
        })


@extend_schema(
    tags=["Authentication"],
    summary="User login",
    description="Authenticate the user and return JWT tokens.",
    request=LoginSerializer,
    responses={
        200: inline_serializer(
            name="LoginResponse",
            fields={
                "refresh": serializers.CharField(),
                "access": serializers.CharField(),
            },
        ),
        400: OpenApiResponse(description="Invalid credentials."),
    },
)
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        logger.info(
            "User %s logged in successfully.",
            user.id
        )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response(
            {
                "refresh": str(refresh),
                "access": str(access),
            }
        )


@extend_schema(
    tags=["Authentication"],
    summary="User logout",
    description="Invalidate the refresh token.",
    request=LogoutSerializer,
    responses={
        205: inline_serializer(
            name="LogoutResponse",
            fields={
                "message": serializers.CharField(),
            },
        ),
        400: inline_serializer(
            name="BadRequestResponse",
            fields={
                "success": serializers.BooleanField(),
                "status_code": serializers.IntegerField(),
                "errors": serializers.DictField(),
            },
        ),
        401: inline_serializer(
            name="UnauthorizedResponse",
            fields={
                "success": serializers.BooleanField(),
                "status_code": serializers.IntegerField(),
                "errors": serializers.DictField(),
            },
        ),
    },
)
class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        logger.info(
            "User %s logged out. IP: %s",
            request.user.id,
            request.META.get("REMOTE_ADDR")
        )

        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_205_RESET_CONTENT
        )


@extend_schema(
    tags=["Profile"],
    summary="Retrieve profile",
    responses={200: ProfileSerializer},
)
@extend_schema(
    methods=["PUT"],
    tags=["Profile"],
    summary="Update profile",
    request=ProfileSerializer,
    responses={200: ProfileSerializer},
)
@extend_schema(
    methods=["PATCH"],
    tags=["Profile"],
    summary="Partially update profile",
    request=ProfileSerializer,
    responses={200: ProfileSerializer},
)
class ProfileAPIView(RetrieveUpdateAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        FormParser,
    ]

    def get_object(self):
        return self.request.user.profile

    def perform_update(self, serializer):
        profile = serializer.save()

        logger.info(
            "Profile %s updated by user %s",
            profile.id,
            self.request.user.id
        )





