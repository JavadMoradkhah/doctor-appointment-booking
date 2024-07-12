from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    SAFE_METHODS,
    AllowAny,
)
from authentication.permissions import IsAdminOrReadOnly, IsDoctor, IsDoctorOwner
from . import serializers
from .models import Doctor, DoctorDegree, Specialization, DoctorSchedule

# Create your views here.


class DoctorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_permissions(self):
        if self.action in ["profile"]:
            return [IsAuthenticated(), IsDoctor()]
        if self.request.method not in SAFE_METHODS:
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        if self.action == "profile":
            return Doctor.objects.select_related(
                "profile", "specialization", "degree"
            ).all()
        return Doctor.objects.all()

    def get_serializer_context(self):
        return {
            "user_id": self.request.user.id,
        }

    def get_serializer_class(self):
        safe_methods = self.request.method in SAFE_METHODS

        if self.action == "profile" and not safe_methods:
            return serializers.DoctorCreateUpdateSerializer

        if self.action == "profile" and safe_methods:
            return serializers.DoctorRetrieveSerializer

        if self.action in ["create", "update"]:
            return serializers.AdminDoctorCreateUpdateSerializer

        return serializers.DoctorListSerializer

    @action(detail=True, methods=["GET", "POST", "PUT", "PATCH"])
    def profile(self, request, pk):

        if self.request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(profile_id=request.user.id)
            return Response(serializers.data)

        if self.request.method in ["PUT", "PATCH"]:
            partial = request.method == "PATCH"
            doctor = get_object_or_404(self.get_queryset(), profile_id=request.user.id)
            serializer = self.get_serializer(
                instance=doctor, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        doctor = get_object_or_404(self.get_queryset(), profile_id=request.user.id)
        serializer = self.get_serializer(doctor)
        return Response(serializer.data)


class DoctorDegreeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = serializers.DoctorDegreeSerializer
    queryset = DoctorDegree.objects.all()


class SpecializationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = serializers.SpecializationSerializer
    queryset = Specialization.objects.all()


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDoctor, IsDoctorOwner]

    def get_queryset(self):
        return (
            DoctorSchedule.objects.filter(doctor_id=self.request.user.id)
            .select_related("medical_center")
            .all()
        )

    def get_serializer_class(self):

        if self.request.method not in SAFE_METHODS:
            return serializers.DoctorScheduleCreateUpdateSerializer
        return serializers.DoctorScheduleListRetrieveSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}
