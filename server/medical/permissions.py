from rest_framework.permissions import BasePermission
from .models import MedicalCenter


class IsManagerOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "manager_id"):
            return request.user.id == obj.manager_id

        return False

    def has_permission(self, request, view):
        view_kwargs = view.kwargs.keys()

        if "manager_pk" not in view_kwargs:
            return True

        return request.user.id == int(view.kwargs["manager_pk"])


class IsManagerMedicalCenterOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "manager_id"):
            return request.user.id == obj.manager_id

        try:
            medical_center = MedicalCenter.objects.get(pk=obj.medical_center_id)
            return request.user.id == medical_center.manager_id
        except MedicalCenter.DoesNotExist:
            return False

    def has_permission(self, request, view):
        view_kwargs = view.kwargs.keys()

        if "medical_center_pk" not in view_kwargs:
            return True

        try:
            medical_center = MedicalCenter.objects.get(
                pk=view.kwargs["medical_center_pk"]
            )
            return request.user.id == medical_center.manager_id
        except MedicalCenter.DoesNotExist:
            return False
