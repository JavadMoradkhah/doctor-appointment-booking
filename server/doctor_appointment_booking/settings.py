from pathlib import Path
from datetime import timedelta
import redis
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', cast=str, default=None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool, default=True)

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', cast=lambda v: [item.strip() for item in v.split(",")], default="*"
)

# Application definition

APPS = [
    'account',
    'authentication'
]

MODULES = [
    'rest_framework',
    'django_cleanup.apps.CleanupConfig',
    'debug_toolbar',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Installed
    *MODULES
    # My Apps
    *APPS
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = [
    "127.0.0.1",
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}

ROOT_URLCONF = 'doctor_appointment_booking.urls'

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

WSGI_APPLICATION = 'doctor_appointment_booking.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        "NAME": config('DB_NAME', cast=str, default='postgres'),
        "USER": config('DB_USER', 'postgres', cast=str, default='postgres'),
        "HOST": config('DB_HOST', '127.0.0.1', cast=int, default='127.0.0.1'),
        "PORT": config('DB_PORT', '5432', cast=int, default=5432),
        "PASSWORD": config('DB_PASSWORD', cast=str, default=None)
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# Main user model class
AUTH_USER_MODEL = 'account.User'


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# JWT authentication settings
JWT_SECRET = config('JWT_SECRET', cast=str, default=None)
JWT_AUDIENCE = config('JWT_AUDIENCE', cast=str, default=None)
JWT_ISSUER = config('JWT_ISSUER', cast=str, default=None)
JWT_REFRESH_TOKEN_COOKIE = 'refresh-token'

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
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

# Redis settings
REDIS = redis.Redis(
    host='redis', port=6379, db=0,
    charset="utf-8", decode_responses=True
)
# Celery broker settings
CELERY_BROKER_URL = 'redis://redis:6379/1'
CELERY_TIMEZONE = 'Asia/Tehran'

# Api key settings
API_KEY_SMS = config('API_KEY_SMS', cast=str, default=None)
