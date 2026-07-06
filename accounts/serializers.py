from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .models import Profile, User
import logging

logger = logging.getLogger(__name__)


class UserRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):

        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password": "Passwords do not match."}
            )

        return attrs


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone = attrs.get('phone')
        password = attrs.get('password')
        user = authenticate(
            phone=phone,
            password=password
        )
        if not user:
            raise serializers.ValidationError('Invalid phone number or password.')
        attrs["user"] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self, **kwargs):
        refresh = self.validated_data["refresh"]

        try:
            token = RefreshToken(refresh)
            token.blacklist()

        except TokenError:
            raise serializers.ValidationError(
                {"refresh": "Refresh token is invalid or expired."}
            )

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "phone",
            "email",
            "first_name",
            "last_name",
        ]
        read_only_fields = fields


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = [
            "user",
            "avatar",
            "bio",
            "address",
            "birth_date",
            "created_at",
        ]
        read_only_fields = ["created_at"]







