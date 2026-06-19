from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
    )
    password_confirm = serializers.CharField(
        write_only=True,
    )
    class Meta:
        model = User

        fields = ('phone', 'email', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate(self, data):
        password = data['password']
        password_confirm = data['password_confirm']
        if password != password_confirm:
            raise serializers.ValidationError({"password":"Passwords dont match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')

        user = User.objects.create_user(**validated_data)
        return user



