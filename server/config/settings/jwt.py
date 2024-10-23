from datetime import timedelta

from decouple import config

# JWT Settings

JWT_SECRET = config("JWT_SECRET")
JWT_AUDIENCE = config("JWT_AUDIENCE")
JWT_ISSUER = config("JWT_ISSUER")
JWT_REFRESH_TOKEN_COOKIE = "refresh-token"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=12),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": JWT_SECRET,
    "AUDIENCE": JWT_AUDIENCE,
    "ISSUER": JWT_ISSUER,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "sub",
    "TOKEN_OBTAIN_SERIALIZER": "authentication.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "authentication.serializers.CookieTokenRefreshSerializer",
}
