from rest_framework import serializers
from .models import User, Profile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "gender", "nation_code", "date_of_birth"]


class UserListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="profile.first_name")
    last_name = serializers.CharField(source="profile.last_name")

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone",
            "role",
            "is_active",
            "joined_at",
        ]


class UserRetrieveSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="profile.first_name")
    last_name = serializers.CharField(source="profile.last_name")
    gender = serializers.CharField(source="profile.gender")
    date_of_birth = serializers.CharField(source="profile.date_of_birth")
    nation_code = serializers.CharField(source="profile.nation_code")

    class Meta:
        model = User
        fields = [
            "id",
            "phone",
            "role",
            "is_active",
            "joined_at",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "nation_code",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "role"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "role"]


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source="user.id")
    phone = serializers.CharField(source="user.phone")
    role = serializers.CharField(source="user.role")
    joined_at = serializers.CharField(source="user.joined_at")

    class Meta:
        model = Profile
        fields = [
            "id",
            "phone",
            "role",
            "joined_at",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "nation_code",
        ]


class ProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "gender", "date_of_birth", "nation_code"]
