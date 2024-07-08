from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

urlpatterns = []

router = DefaultRouter()

router.register(r"provinces", views.ProvinceViewSet, basename="provinces")

router.register(r"cities", views.CityViewSet, basename="cities")

router.register(r"insurance", views.InsuranceViewSet, basename="insurance")

router.register(r"my-insurances", views.UserInsuranceViewSet, basename="my-insurances")

province_router = routers.NestedSimpleRouter(router, r"provinces", lookup="province")

province_router.register(r"cities", views.ProvinceCitiesViewSet, basename="cities")

urlpatterns += router.urls

urlpatterns += province_router.urls
