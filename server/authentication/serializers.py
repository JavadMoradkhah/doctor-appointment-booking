from typing import Any, Dict
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer,
)
from .enums import UrlTargetRole

User = get_user_model()


class PhoneSerializer(serializers.Serializer):
    phone = serializers.RegexField(
        regex=r"^09([0-9]{9})$", min_length=11, max_length=11
    )


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Replacing the username field with a new one that has validation
        self.fields[self.username_field] = serializers.RegexField(
            r"^09([0-9]{9})$", min_length=11, max_length=11
        )
        # Adding the otp field to the serializer
        self.fields["otp"] = serializers.RegexField(
            r"[0-9]{6}$", min_length=6, max_length=6
        )
        # We dont need the password field so we can remove it
        del self.fields["password"]

    def validate(self, attrs: Dict[str, Any]) -> Dict[Any, Any]:
        phone = attrs["phone"]
        otp_code = attrs["otp"]

        url_target_role = self.context.get("url_target", UrlTargetRole.PATIENT.value)

        cache_key = f"otp:{phone}"

        otp_in_cache = settings.REDIS.get(cache_key)

        if not otp_in_cache:
            raise AuthenticationFailed(
                detail="کد تایید به شماره موبایل داده شده ارسال نشده یا منقضی شده است"
            )

        if otp_code != otp_in_cache:
            raise ValidationError("کد تایید وارد شده نامعتبر است")

        # Removing the otp code from Redis so it can not be used again
        settings.REDIS.delete(cache_key)

        user, created = User.objects.get_or_create(
            phone=phone, defaults={"role": url_target_role}
        )

        if not created and not user.is_active:
            raise AuthenticationFailed("حساب کاربری شما غیر فعال شده است")

        refresh = self.get_token(user)

        data = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["phone"] = user.phone
        token["role"] = user.role
        return token


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get(
            settings.JWT_REFRESH_TOKEN_COOKIE
        )

        if not attrs["refresh"]:
            raise NotAuthenticated("وارد حساب کاربری خود شوید")

        return super().validate(attrs)
