from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import View
from typing import Any


User = get_user_model()


class IsNotAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return not super().has_permission(request, view)


class IsManager(BasePermission):
    """
    Permission to check if the user is a manager.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_manager


class IsDoctor(BasePermission):
    """
    Permission to check if the user is a doctor.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_doctor


class IsDoctorOrAdmin(BasePermission):
    """
    Permission to allow doctors or admin users.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_doctor or request.user.is_admin


class IsDoctorOwner(BasePermission):
    """
    Permission to check if the request user is the owner of the doctor resource.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        doctor_pk = view.kwargs.get("doctor_pk")
        return not doctor_pk or request.user.id == int(doctor_pk)

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return request.user.id == obj.doctor_id


class IsDoctorOrPatient(BasePermission):
    """
    Permission to allow either doctors or patients.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_doctor or request.user.is_patient


class IsPatientOwner(BasePermission):
    """
    Permission to check if the request user is the owner of the patient resource.
    """
    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return request.user.id == obj.patient_id


class IsPatient(BasePermission):
    """
    Permission to check if the user is a patient.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_patient


class IsUserOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj.id == request.user.id

        return obj.user_id == request.user.id

    def has_permission(self, request, view):
        view_kwargs = view.kwargs.keys()

        if "user_pk" in view_kwargs:
            return request.user.id == int(view.kwargs["user_pk"])

        return bool("pk" in view_kwargs and request.user.id == int(view.kwargs["pk"]))


class IsAdminOrReadOnly(BasePermission):
    """
    Permission that allows access to safe methods (GET, HEAD, OPTIONS) for everyone,
    but restricts write methods to admin users.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff
