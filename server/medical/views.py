from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAuthenticated,
    IsAdminUser,
    AllowAny,
)
from authentication.permissions import (
    IsAdminOrReadOnly,
    IsPatient,
    IsManager,
)
from .models import (
    Province,
    City,
    Insurance,
    UserInsurance,
    Facility,
    MedicalCenter,
    MedicalCenterStatus,
    MedicalCenterGallery,
    MedicalCenterAddress,
    MedicalCenterSchedule,
    MedicalCenterTelephone,
)
from .permissions import IsManagerMedicalCenterOwner
from . import serializers


class ProvinceViewSet(viewsets.ModelViewSet):
    queryset = Province.objects.order_by("name").all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return serializers.ProvinceCreateUpdateSerializer

        if self.action == "retrieve":
            return serializers.ProvinceRetrieveSerializer

        return serializers.ProvinceListSerializer


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("province").order_by("name").all()
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

    def get_queryset(self):
        return (
            UserInsurance.objects.filter(user_id=self.request.user.id)
            .select_related("insurance")
            .all()
        )

    def get_serializer_class(self):
        if self.request.method not in SAFE_METHODS:
            return serializers.UserInsuranceCreateUpdateSerializer
        return serializers.UserInsuranceListRetrieveSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = serializers.FacilitySerializer
    permission_classes = [IsAdminOrReadOnly]


class MedicalCenterViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = MedicalCenter.objects.all()

        if self.request.method not in SAFE_METHODS:
            return queryset

        if self.action == "retrieve":
            queryset = queryset.select_related("address").all()
            queryset = queryset.prefetch_related("telephones", "gallery").all()

        if self.is_admin_user():
            queryset = queryset.select_related("manager__profile__user", "status")

        return queryset.select_related("facility", "city")

    def get_permissions(self):
        if self.action == "status":
            return [IsAuthenticated(), IsAdminUser()]

        if self.request.method in SAFE_METHODS:
            return [AllowAny()]

        return [IsAuthenticated(), IsManager(), IsManagerMedicalCenterOwner()]

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "status":
            return serializers.MedicalCenterStatusUpdateSerializer

        if self.request.method not in SAFE_METHODS:
            return serializers.MedicalCenterCreateUpdateSerializer

        if self.action == "retrieve" and not self.is_admin_user():
            return serializers.MedicalCenterRetrieveSerializer

        if self.action == "retrieve" and self.is_admin_user():
            return serializers.AdminMedicalCenterRetrieveSerializer

        if self.action == "list" and self.is_admin_user():
            return serializers.AdminMedicalCenterListSerializer

        return serializers.MedicalCenterListSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}

    def is_admin_user(self):
        return bool(
            self.request.user
            and self.request.user.is_authenticated
            and self.request.user.is_staff
        )

    @action(detail=True, methods=["PUT", "PATCH"])
    def status(self, request, pk):
        partial = request.method == "PATCH"
        status = get_object_or_404(MedicalCenterStatus, pk=pk)
        serializer = self.get_serializer(status, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.validated_data)


class MedicalCenterGallery(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = MedicalCenterGallery.objects.all()
    permission_classes = [IsAuthenticated, IsManager, IsManagerMedicalCenterOwner]
    serializer_class = serializers.MedicalCenterGallerySerializer

    def get_serializer_context(self):
        return {"medical_center_id": self.kwargs["medical_center_pk"]}


class MedicalCenterTelephoneViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated, IsManager, IsManagerMedicalCenterOwner]
    serializer_class = serializers.MedicalCenterTelephoneSerializer

    def get_queryset(self):
        return MedicalCenterTelephone.objects.filter(
            medical_center_id=self.kwargs["medical_center_pk"]
        ).all()

    def get_serializer_context(self):
        return {"medical_center_id": self.kwargs["medical_center_pk"]}


class MedicalCenterAddressViewSet(
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.MedicalCenterAddressSerializer
    permission_classes = [IsAuthenticated, IsManager, IsManagerMedicalCenterOwner]

    def get_queryset(self):
        return MedicalCenterAddress.objects.filter(
            medical_center_id=self.kwargs["medical_center_pk"]
        ).all()

    def get_serializer_context(self):
        return {"medical_center_id": self.kwargs["medical_center_pk"]}


class MedicalCenterScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsManager, IsManagerMedicalCenterOwner]
    serializer_class = serializers.MedicalCenterScheduleSerializer

    def get_queryset(self):
        return MedicalCenterSchedule.objects.filter(
            medical_center_id=self.kwargs["medical_center_pk"]
        ).all()

    def get_serializer_context(self):
        return {"medical_center_id": self.kwargs["medical_center_pk"]}
