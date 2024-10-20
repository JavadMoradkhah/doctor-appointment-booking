from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import View
from typing import Any


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
    """
    Permission to check if the request user owns the user resource.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.id == int(view.kwargs["pk"])

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return request.user.id == obj.user_id


class IsAdminOrReadOnly(BasePermission):
    """
    Permission that allows access to safe methods (GET, HEAD, OPTIONS) for everyone,
    but restricts write methods to admin users.
    """
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_staff
