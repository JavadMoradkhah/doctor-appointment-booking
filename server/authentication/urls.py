from django.urls import path
from . import views

urlpatterns = [
    path('otp/', views.SendOtpView.as_view()),
    path(
        'login/',
        views.CookieTokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'refresh/',
        views.CookieTokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
