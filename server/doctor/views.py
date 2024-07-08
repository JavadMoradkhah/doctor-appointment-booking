from .models import Doctor, DoctorDegree, Specialization
from rest_framework import viewsets
from authentication.permissions import IsAdminOrReadOnly, IsDoctor, IsPatient
from rest_framework.permissions import IsAuthenticated, IsAdminUser, SAFE_METHODS
from . import serializers
from django.shortcuts import get_object_or_404
from account.models import Profile
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.


class DoctorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_permissions(self):
        if self.action in ["profile"]:
            return [IsAuthenticated(), IsDoctor()]
        if self.request.method not in SAFE_METHODS:
            return [IsAuthenticated(), IsAdminUser()]
        return []

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
        is_safe_method = self.request.method in SAFE_METHODS

        if self.action == "profile" and not is_safe_method:
            return serializers.DoctorCreateUpdateSerializer

        if self.action == "profile" and is_safe_method:
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
