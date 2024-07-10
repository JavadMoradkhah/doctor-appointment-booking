from django.urls import path
from .enums import UrlTargetRole
from . import views

urlpatterns = [
    path("otp/", views.SendOtpView.as_view(), name="otp"),
    path("login/", views.CookieTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "doctors/login/",
        views.CookieTokenObtainPairView.as_view(),
        {"url_target": UrlTargetRole.DOCTOR.value},
        name="login-doctors",
    ),
    path(
        "managers/login/",
        views.CookieTokenObtainPairView.as_view(),
        {"url_target": UrlTargetRole.MANAGER.value},
        name="login-managers",
    ),
    path("refresh/", views.CookieTokenRefreshView.as_view(), name="token_refresh"),
]
