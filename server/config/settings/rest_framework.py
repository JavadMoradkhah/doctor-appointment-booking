# Django REST Framework Settings

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "config.settings.pagination.NeatPagination",
    "PAGE_SIZE": 100,
}
