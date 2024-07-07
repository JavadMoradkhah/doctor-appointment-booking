from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAdminUser
from authentication.permissions import IsAdminOrReadOnly, IsPatient
from .models import Province, City, Insurance, UserInsurance
from . import serializers


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.order_by('name').all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return serializers.ProvinceCreateUpdateSerializer

        if self.action == 'retrieve':
            return serializers.ProvinceRetrieveSerializer

        return serializers.ProvinceListSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related('province').order_by('name').all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return serializers.CityCreateUpdateSerializer
        return serializers.CityListRetrieveSerializer


class ProvinceCitiesViewSet(viewsets.ViewSet):
    serializer_class = serializers.ProvinceCitiesListSerializer

    def list(self, request, province_pk):
        cities = City.objects.filter(province_id=province_pk).all()
        serializer = self.serializer_class(cities, many=True)
        return Response(serializer.data)


class InsuranceViewSet(viewsets.ModelViewSet):
    queryset = Insurance.objects.all()
    serializer_class = serializers.InsuranceSerializer
    permission_classes = [IsAdminOrReadOnly]


class UserInsuranceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsPatient]
    serializer_class = serializers.UserInsuranceSerializer

    def get_queryset(self):
        return UserInsurance.objects.filter(
            user_id=self.request.user.id
        ).select_related('insurance').all()

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return serializers.UserInsuranceCreateUpdateSerializer
        return serializers.UserInsuranceListRetrieveSerializer

    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id
        }

    def create(self, request, *args, **kwargs):
        if UserInsurance.objects.filter(user_id=request.user.id).count() >= 2:
            raise APIException(
                detail='امکان ثبت بیشتراز 2 بیمه وجود ندارد',
                code=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
