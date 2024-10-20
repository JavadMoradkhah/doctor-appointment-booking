from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)

# Fetch the User model dynamically
User = get_user_model()


class PhoneSerializer(serializers.Serializer):
    """
    Serializer for validating phone numbers. It expects a phone number that starts with '09'
    and has a total length of 11 digits.
    """
    phone: serializers.RegexField = serializers.RegexField(
        regex=r"^09([0-9]{9})$", min_length=11, max_length=11
    )


class SignupSerializer(serializers.ModelSerializer):
    """
    Serializer for user signup. Validates necessary fields including OTP code.
    """
    otp_code: serializers.RegexField = serializers.RegexField(r"[0-9]{6}$")

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "nation_code",
            "gender",
            "date_of_birth",
            "phone",
            "otp_code",
        ]


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer that overrides the default behavior to authenticate using
    a phone number and OTP instead of username/password.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Replace the username field with phone number validation
        self.fields[self.username_field] = serializers.RegexField(
            r"^09([0-9]{9})$", min_length=11, max_length=11
        )
        # Add the OTP field for validation
        self.fields["otp"] = serializers.RegexField(
            r"[0-9]{6}$", min_length=6, max_length=6
        )
        # Remove the password field since it's not used in OTP-based authentication
        del self.fields["password"]

    @classmethod
    def get_token(cls, user: User) -> dict:
        """
        Generate a JWT token for the user and add custom fields (phone, role) to the payload.
        """
        token = super().get_token(user)
        token["phone"] = user.phone
        token["role"] = user.role
        return token


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Serializer for handling token refresh using cookies. If the refresh token is missing,
    it raises an authentication error.
    """
    refresh: str = None

    def validate(self, attrs: dict) -> dict:
        # Extract the refresh token from cookies
        attrs["refresh"] = self.context["request"].COOKIES.get(
            settings.JWT_REFRESH_TOKEN_COOKIE
        )

        # If the refresh token is not found in cookies, raise an error
        if not attrs["refresh"]:
            raise NotAuthenticated("وارد حساب کاربری خود شوید")

        # Proceed with the normal validation process
        return super().validate(attrs)
