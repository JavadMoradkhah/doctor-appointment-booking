from rest_framework import viewsets, status
from authentication.permissions import IsAdminOrReadOnly, IsPatient
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Province, City, Insurance, UserInsurance
from . import serializers
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import APIException
# Create your views here.


class ProvinceViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    queryset = Province.objects.all()
    serializer_class = serializers.ProvinceSerializer


class CityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    queryset = City.objects.all()

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


class InsuranceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    serializer_class = serializers.InsuranceSerializer
    queryset = Insurance.objects.all()


class UserInsuranceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsPatient]
    serializer_class = serializers.UserInsuranceSerializer

    def get_queryset(self):
        queryset = UserInsurance.objects.filter(
            user_id=self.request.user.id).all()
        return queryset

    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id
        }

    def create(self, request, *args, **kwargs):
        if UserInsurance.objects.filter(user_id=request.user.id).count() >= 2:
            raise APIException(
                detail='امکان ثبت بیشتراز 2 بیمه را ندارید', code=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
