from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsUserOwnsMedicalCenter(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.manager_id
