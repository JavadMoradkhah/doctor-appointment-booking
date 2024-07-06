from . import serializers
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from account.models import Profile

User = get_user_model()


class UserViewSet(ModelViewSet):
    def get_permissions(self):
        if self.action in ['me', 'create_profile', 'update_profile']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsAdminUser()]

    def get_queryset(self):
        queryset = User.objects.all()

        if self.action in ['list', 'retrieve']:
            return queryset.select_related('profile')

        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.UserRetrieveSerializer

        if self.action == 'me':
            return serializers.ProfileSerializer

        if self.action in ['create_profile', 'update_profile']:
            return serializers.ProfileCreateUpdateSerializer

        if self.action == 'create':
            return serializers.UserCreateSerializer

        if self.action == 'update':
            return serializers.UserUpdateSerializer

        return serializers.UserListSerializer

    @action(detail=True, methods=['PATCH'])
    def activate(self, request: Request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['PATCH'])
    def deactivate(self, request: Request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'])
    def me(self, request: Request):
        user = get_object_or_404(self.get_queryset(), pk=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def create_profile(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user.id)
        return Response(serializer.data)

    @action(detail=False, methods=['PUT', 'PATCH'])
    def update_profile(self, request: Request, *args, **kwargs):
        partial = request.method == 'PATCH'
        profile = get_object_or_404(Profile, user_id=request.user.id)
        serializer = self.get_serializer(
            profile, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
