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
from .enums import OtpSettings
from .models import Otp, OtpBlacklist
from .otp_utils import hash_otp, verify_otp
from .serializers import PhoneSerializer, SignupSerializer
from .tasks import send_otp

User = get_user_model()


class SendOtpView(GenericAPIView):
    """
    Sends an OTP to the user's phone number and manages blacklist and OTP attempt handling.
    """
    queryset = User.objects.all()
    serializer_class = PhoneSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone: str = serializer.validated_data["phone"]
        current_time: datetime = timezone.now()

        # Check if the phone number is in the blacklist
        blacklist_entry: OtpBlacklist = OtpBlacklist.objects.filter(phone=phone).first()
        if blacklist_entry and blacklist_entry.expires_at > current_time:
            raise ValidationError(
                detail=f"شماره شما تا تاریخ {blacklist_entry.expires_at.strftime('%Y-%m-%d %H:%M:%S')} در لیست سیاه قرار دارد.",
                code=status.HTTP_403_FORBIDDEN
            )

        # Check if an OTP was already sent and is still valid
        otp_entry: Otp = Otp.objects.filter(phone=phone).first()
        if otp_entry and otp_entry.expires_at > current_time:
            otp_entry.attempts += 1
            otp_entry.save()

            # Blacklist the phone if max attempts are reached
            if otp_entry.attempts >= OtpSettings.MAX_ATTEMPTS.value:
                OtpBlacklist.objects.update_or_create(
                    phone=phone,
                    defaults={"expires_at": current_time + timedelta(minutes=2)}
                )
            raise Throttled(detail="کد ارسال شده هنوز منقضی نشده است.")

        # Generate and hash OTP
        otp_code: str = str(randint(111111, 999999))
        if settings.DEBUG:
            print(f"OTP Code: {otp_code}")
        else:
            send_otp.delay(phone, otp_code)

        hashed_otp: str = hash_otp(otp_code)
        expires_at: datetime = current_time + timedelta(minutes=OtpSettings.OTP_EXPIRATION_TIME.value)

        # Save or update OTP in the database
        with transaction.atomic():
            Otp.objects.update_or_create(
                phone=phone,
                defaults={
                    'code': hashed_otp,
                    'expires_at': expires_at,
                    'attempts': 0
                }
            )

        return Response(status=status.HTTP_200_OK)


class SignupView(GenericAPIView):
    """
    Handles user signup using OTP verification.
    """
    serializer_class = SignupSerializer

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone: str = serializer.validated_data["phone"]
        otp_code: str = serializer.validated_data["otp_code"]

        otp: Otp = get_object_or_404(Otp, phone=phone)

        # Verify OTP expiration and validity
        if timezone.now() >= otp.expires_at:
            raise AuthenticationFailed("کد تایید به شماره موبایل داده شده ارسال نشده یا منقضی شده است.")

        if not verify_otp(otp.code, otp_code):
            return Response("کد تایید وارد شده نامعتبر است.", status=status.HTTP_403_FORBIDDEN)

        otp.delete()

        # Create a new user
        validated_data: Dict[str, Any] = serializer.validated_data
        validated_data.pop("otp_code", None)
        user: User = User.objects.create_user(**validated_data, role=USER_ROLE_PATIENT)

        # Generate JWT token
        refresh: RefreshToken = RefreshToken.for_user(user)
        data: Dict[str, str] = {"access": str(refresh.access_token)}

        # Send token in the response
        response: Response = Response(data, status=status.HTTP_201_CREATED)
        response.set_cookie(
            key=settings.JWT_REFRESH_TOKEN_COOKIE,
            value=refresh,
            max_age=jwt_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            httponly=True,
        )

        return response


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that handles OTP-based login.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        phone: str = request.data.get("phone")
        otp_code: str = request.data.get("otp")

        otp: Otp = get_object_or_404(Otp, phone=phone)

        # Verify OTP expiration and validity
        if timezone.now() >= otp.expires_at:
            raise AuthenticationFailed("کد تایید به شماره موبایل داده شده ارسال نشده یا منقضی شده است.",
                                       code=status.HTTP_403_FORBIDDEN)

        if not verify_otp(otp.code, otp_code):
            return Response("کد تایید وارد شده نامعتبر است.", status=status.HTTP_403_FORBIDDEN)

        otp.delete()

        # Get the user and check account status
        user: User = get_object_or_404(User, phone=phone)
        if not user.is_active:
            raise AuthenticationFailed("حساب کاربری شما غیر فعال شده است.")

        # Generate JWT token
        refresh: RefreshToken = self.get_serializer().get_token(user)
        access: str = str(refresh.access_token)

        # Send token in response with JWT refresh token in the cookie
        response: Response = Response({"access": access}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.JWT_REFRESH_TOKEN_COOKIE,
            value=str(refresh),
            max_age=jwt_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            httponly=True,
        )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    Refreshes the JWT token and sets it in a cookie.
    """

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh: str = serializer.validated_data["refresh"]

        # Return new access token and set refresh token in the cookie
        response: Response = Response({"access": serializer.validated_data["access"]}, status=status.HTTP_200_OK)
        response.set_cookie(
            key=settings.JWT_REFRESH_TOKEN_COOKIE,
            value=refresh,
            max_age=jwt_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            httponly=True,
        )

        return response
