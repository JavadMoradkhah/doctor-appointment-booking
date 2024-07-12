from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

urlpatterns = []

router = DefaultRouter()

router.register(r"provinces", views.ProvinceViewSet, basename="provinces")

router.register(r"cities", views.CityViewSet, basename="cities")

router.register(r"insurance", views.InsuranceViewSet, basename="insurance")

router.register(r"my-insurances", views.UserInsuranceViewSet, basename="my-insurances")

router.register(r"facilities", views.FacilityViewSet, basename="facilities")

router.register(
    r"medical-centers", views.MedicalCenterViewSet, basename="medical-centers"
)

# Provinces Router
province_router = routers.NestedSimpleRouter(router, r"provinces", lookup="province")
province_router.register(r"cities", views.ProvinceCitiesViewSet, basename="cities")

medical_center_router = routers.NestedSimpleRouter(
    router, r"medical-centers", lookup="medical_center"
)
medical_center_router.register(
    r"gallery", views.MedicalCenterGallery, basename="medical-center-gallery"
)

medical_center_router.register(
    r"telephones",
    views.MedicalCenterTelephoneViewSet,
    basename="medical-center-telephones",
)

medical_center_router.register(
    r"address",
    views.MedicalCenterAddressViewSet,
    basename="medical-center-address",
)

medical_center_router.register(
    r"schedules",
    views.MedicalCenterScheduleViewSet,
    basename="medical-center-schedules",
)

urlpatterns += router.urls
urlpatterns += province_router.urls
urlpatterns += medical_center_router.urls
