from rest_framework import viewsets
from authentication.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Province, City
from .pagination import Pagination
from . import serializers
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
# Create your views here.


class ProvinceApiView(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    queryset = Province.objects.all()
    serializer_class = serializers.ProvinceSerializer
    pagination_class = Pagination


class CityApiView(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    queryset = City.objects.all()
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return serializers.CityCreateUpdateSerializer
        return serializers.CityListRetrieveSerializer


class ProvinceCitiesViewSet(viewsets.ViewSet):
    serializer_class = serializers.ProvinceCitiesListSerializer

    def list(self, request, province_pk):
        cities = City.objects.filter(province__id=province_pk).all()
        serializer = self.serializer_class(cities, many=True)
        return Response(serializer.data)
