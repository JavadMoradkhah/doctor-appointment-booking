from random import randint
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import Throttled, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings as jwt_settings
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from account import choices
from .serializers import PhoneSerializer
from .tasks import send_otp

User = get_user_model()


class SendOtpView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = PhoneSerializer

    def post(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']

        cache_key = f'otp:{phone}'

        otp_in_cache = settings.REDIS.get(cache_key)

        if otp_in_cache:
            raise Throttled(detail='کد ارسال شده هنوز منقضی نشده است')

        otp_code = str(randint(111111, 999999))

        if settings.DEBUG:
            print('OTP Code:', otp_code)
        else:
            send_otp.delay(phone, otp_code)

        settings.REDIS.set(cache_key, otp_code, ex=2 * 60)

        return Response(status=status.HTTP_200_OK)


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']

        user = User.objects.filter(phone=phone).get()

        if user and not user.is_active:
            raise AuthenticationFailed('حساب کاربری شما غیر فعال شده است')

        if not user:
            user = User.objects.create_user(
                phone=phone,
                role=choices.USER_ROLE_PATIENT
            )

        # Issuing user tokens
        refresh = RefreshToken.for_user(user)

        response = Response(
            {'access': str(refresh.access_token)},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key=settings.JWT_REFRESH_TOKEN_COOKIE,
            value=str(refresh),
            max_age=jwt_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            httponly=True
        )

        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data['refresh']

        response = Response(
            {'access': serializer.validated_data['access']},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key=settings.JWT_REFRESH_TOKEN_COOKIE,
            value=refresh,
            max_age=jwt_settings.REFRESH_TOKEN_LIFETIME.total_seconds(),
            httponly=True
        )

        return response
