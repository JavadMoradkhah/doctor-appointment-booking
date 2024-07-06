from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_doctor
