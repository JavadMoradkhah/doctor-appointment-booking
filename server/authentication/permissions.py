from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


User = get_user_model()


class IsNotAuthenticated(IsAuthenticated):
    def has_permission(self, request, view):
        return not super().has_permission(request, view)


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor


class IsDoctorOwner(BasePermission):
    def has_permission(self, request, view):
        view_kwargs = view.kwargs.keys()
        if "doctor_pk" not in view_kwargs:
            return True
        return request.user.id == int(view.kwargs["doctor_pk"])

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.doctor_id


class IsPatient(BasePermission):
    def has_permission(self, request, view):
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
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )
