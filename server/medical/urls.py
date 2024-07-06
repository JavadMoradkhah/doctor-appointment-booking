from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_nested import routers

urlpatterns = []

router = DefaultRouter()
router.register(r'provinces', views.ProvinceViewSet, basename='province')
router.register(r'city', views.CityViewSet, basename='city')


province_router = routers.NestedSimpleRouter(router, r'provinces', lookup='province')
province_router.register(r'cities', views.ProvinceCitiesViewSet, basename='cities')


urlpatterns += router.urls

urlpatterns += province_router.urls