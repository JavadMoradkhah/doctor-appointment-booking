import os
from pathlib import Path
from datetime import timedelta
from decouple import config
import redis

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = config('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = config(
    'DJANGO_ALLOWED_HOSTS',
    cast=lambda value: [item.strip() for item in value.split(',')],
    default='*'
)

# Installed Apps List

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_cleanup.apps.CleanupConfig',
    'debug_toolbar',
]

MY_APPS = [
    'account',
    'authentication'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *MY_APPS
]

# Request Processing Pipeline

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'doctor_appointment_booking.urls'

WSGI_APPLICATION = 'doctor_appointment_booking.wsgi.application'

# Templates Settings

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database Settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": config('DB_NAME'),
        "USER": config('DB_USER', default='postgres'),
        "HOST": config('DB_HOST', default='127.0.0.1'),
        "PORT": config('DB_PORT', default='5432'),
        "PASSWORD": config('DB_PASSWORD')
    }
}

# Authentication

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'account.User'

# Internationalization

LANGUAGE_CODE = 'fa-IR'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework Settings

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# JWT Settings

JWT_SECRET = config('JWT_SECRET')
JWT_AUDIENCE = config('JWT_AUDIENCE')
JWT_ISSUER = config('JWT_ISSUER')
JWT_REFRESH_TOKEN_COOKIE = 'refresh-token'

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

    "TOKEN_OBTAIN_SERIALIZER": "authentication.serializers.TokenObtainSerializer",
    "TOKEN_REFRESH_SERIALIZER": "authentication.serializers.CookieTokenRefreshSerializer"
}

# Redis Settings

REDIS = redis.Redis(
    host='redis', port=6379, db=0,
    charset="utf-8", decode_responses=True
)

# Celery Settings

CELERY_BROKER_URL = 'redis://redis:6379/1'
CELERY_TIMEZONE = 'Asia/Tehran'

# API Keys

API_KEY_SMS = config('API_KEY_SMS')
