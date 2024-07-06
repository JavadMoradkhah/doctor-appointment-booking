from rest_framework import routers
from . import views

urlpatterns = []

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
urlpatterns += router.urls
