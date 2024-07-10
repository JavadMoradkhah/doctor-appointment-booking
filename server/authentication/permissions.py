from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_manager


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_patient


class IsUserOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.id == int(view.kwargs["pk"])

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user_id


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated and request.user.is_staff
        )
