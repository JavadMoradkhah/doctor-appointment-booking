from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAdminUser
from authentication.permissions import IsUserOwner
from account.models import Profile
from . import serializers

User = get_user_model()


class UserViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action == "profile":
            return [IsAuthenticated(), IsUserOwner()]
        return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        is_safe_method = self.request.method in SAFE_METHODS

        if self.action == "profile" and is_safe_method:
            return Profile.objects.select_related("user").all()

        if self.action == "profile" and not is_safe_method:
            return Profile.objects.all()

        if not is_safe_method:
            return User.objects.all()

        return User.objects.select_related("profile").all()

    def get_serializer_class(self):
        is_safe_method = self.request.method in SAFE_METHODS

        if self.action == "profile" and is_safe_method:
            return serializers.ProfileSerializer

        if self.action == "profile" and not is_safe_method:
            return serializers.ProfileCreateUpdateSerializer

        if self.action == "retrieve":
            return serializers.UserRetrieveSerializer

        if self.action == "create":
            return serializers.UserCreateSerializer

        if self.action == "update":
            return serializers.UserUpdateSerializer

        return serializers.UserListSerializer

    def destroy(self, request, *args, **kwargs):
        if request.user.id == int(kwargs["pk"]):
            raise PermissionDenied("شما امکان حذف حساب کاربری خود را ندارید")

        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["PATCH"])
    def activate(self, request: Request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["PATCH"])
    def deactivate(self, request: Request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["GET", "POST", "PUT", "PATCH"])
    def profile(self, request: Request, pk):
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_id=pk)
            return Response(serializer.data)

        if request.method in ["PUT", "PATCH"]:
            partial = request.method == "PATCH"
            profile = get_object_or_404(Profile, user_id=pk)
            serializer = self.get_serializer(
                profile, data=request.data, partial=partial
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        user = get_object_or_404(Profile, pk=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
