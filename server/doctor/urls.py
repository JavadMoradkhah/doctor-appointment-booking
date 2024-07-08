from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

urlpatterns = []

router = DefaultRouter()

router.register(r"doctors", views.DoctorViewSet, basename="profile")

router.register(r"degree", views.DoctorDegreeViewSet, basename="doctor-degree")

router.register(
    r"specialization", views.SpecializationViewSet, basename="doctor-specialization"
)


urlpatterns += router.urls
