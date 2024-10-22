from datetime import datetime, timedelta
from typing import Dict, Any

from django.db import transaction
from django.utils import timezone
from random import randint
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import Throttled, AuthenticationFailed, ValidationError
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from account.choices import USER_ROLE_PATIENT
from config.settings.otp import OTP_SETTINGS
from .models import Otp, OtpBlacklist
from .otp_utils import hash_otp, verify_otp
from .serializers import PhoneSerializer, SignupSerializer
from .tasks import send_otp

User = get_user_model()


class SendOtpView(GenericAPIView):
    """ Sends OTP and manages blacklist and OTP attempt handling """
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone: str = serializer.validated_data["phone"]
        current_time: datetime = timezone.now()

        # Check if the user is blacklisted
        blacklist_entry = OtpBlacklist.objects.filter(phone=phone).last()

        if blacklist_entry:
            if blacklist_entry.expires_at and blacklist_entry.expires_at > current_time:
                return Response(
                    f"تا تاریخ {blacklist_entry.expires_at.strftime('%Y-%m-%d %H:%M:%S')} در لیست سیاه قرار دارید.",
                    status=status.HTTP_403_FORBIDDEN)

            if blacklist_entry.expires_at is None:
                return Response("برای همیشه در لیست سیاه قرار گرفته‌اید.", status=status.HTTP_403_FORBIDDEN)

        otp_entry = Otp.objects.filter(phone=phone).first()
        if otp_entry:
            otp_entry.attempts += 1
            otp_entry.save()

            # If too many attempts, blacklist the user
            time_difference = otp_entry.last_attempt - otp_entry.first_attempt
            if time_difference.days <= 1 and otp_entry.attempts >= OTP_SETTINGS['MAX_ATTEMPTS']:
                user_blacklist_count = OtpBlacklist.objects.filter(phone=phone).count()

                expires_at = \
                    None if user_blacklist_count >= 3 else (
                            current_time + timedelta(
                        hours=(OTP_SETTINGS['BLACKLIST_MULTIPLIER'] * user_blacklist_count))
                    )

                OtpBlacklist.objects.create(phone=phone, expires_at=expires_at)

                raise Throttled("تعداد دفعات بیش از حد و شماره شما به لیست سیاه اضافه شد.")

            raise Throttled("کد ارسال شده هنوز منقضی نشده است.")

        otp_code = str(randint(111111, 999999))
        if settings.DEBUG:
            print(f"OTP Code: {otp_code}")
        else:
            send_otp.delay(phone, otp_code)

        hashed_otp = hash_otp(otp_code)

        expires_at = current_time + timedelta(minutes=OTP_SETTINGS['OTP_EXPIRATION_TIME'])

        Otp.objects.update_or_create(phone=phone, defaults={'code': hashed_otp, 'expires_at': expires_at})

        return Response(status=status.HTTP_200_OK)


class SignupView(GenericAPIView):
    """ Handles user signup with OTP verification """
    serializer_class = SignupSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone: str = serializer.validated_data["phone"]
        otp_code: str = serializer.validated_data["otp_code"]
        otp: Otp = Otp.objects.filter(phone=phone).first()

        if timezone.now() >= otp.expires_at:
            raise AuthenticationFailed("کد تایید ارسال نشده یا منقضی شده است.")

        if not verify_otp(otp.code, otp_code):
            return Response("کد تایید نامعتبر است.", status=status.HTTP_403_FORBIDDEN)

        otp.delete()

        validated_data: Dict[str, Any] = serializer.validated_data
        validated_data.pop("otp_code", None)
        user: User = User.objects.create_user(**validated_data, role=USER_ROLE_PATIENT)

        refresh: RefreshToken = RefreshToken.for_user(user)
        response: Response = Response({"access": str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        response.set_cookie(
            key=settings.JWT_REFRESH_TOKEN_COOKIE,
            value=str(refresh),
            max_age=jwt_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            httponly=True,
        )

        return response


class CookieTokenObtainPairView(TokenObtainPairView):
    """ Custom JWT login with OTP verification """

    def post(self, request: Request, *args, **kwargs) -> Response:
        phone: str = request.data.get("phone")
        otp_code: str = request.data.get("otp")

        otp: Otp = get_object_or_404(Otp, phone=phone)

        if timezone.now() >= otp.expires_at:
            raise AuthenticationFailed("کد تایید ارسال نشده یا منقضی شده است.", code=status.HTTP_403_FORBIDDEN)

        if not verify_otp(otp.code, otp_code):
            return Response("کد تایید نامعتبر است.", status=status.HTTP_403_FORBIDDEN)

        otp.delete()

        user: User = get_object_or_404(User, phone=phone)
        if not user.is_active:
            raise AuthenticationFailed("حساب کاربری غیر فعال شده است.")

        refresh: RefreshToken = self.get_serializer().get_token(user)
        response: Response = Response({"access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.JWT_REFRESH_TOKEN_COOKIE,
            value=str(refresh),
            max_age=jwt_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            httponly=True,
        )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    """ Refreshes JWT token and sets it in a cookie """

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh: str = serializer.validated_data["refresh"]
        response: Response = Response({"access": serializer.validated_data["access"]}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.JWT_REFRESH_TOKEN_COOKIE,
            value=refresh,
            max_age=jwt_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            httponly=True,
        )

        return response
