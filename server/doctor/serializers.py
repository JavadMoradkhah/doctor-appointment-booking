from rest_framework import serializers
from .models import Doctor, DoctorDegree, Specialization
from account.models import Profile
from . import validators


class DoctorListSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(source="specialization.name")
    degree = serializers.CharField(source="degree.degree")
    first_name = serializers.CharField(source="profile.first_name")
    last_name = serializers.CharField(source="profile.last_name")

    class Meta:
        model = Doctor
        fields = [
            "id",
            "first_name",
            "last_name",
            "specialization",
            "degree",
            "biography",
            "avatar",
            "medical_system_number",
        ]


class DoctorRetrieveSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(source="specialization.name")
    degree = serializers.CharField(source="degree.degree")
    first_name = serializers.CharField(source="profile.first_name")
    last_name = serializers.CharField(source="profile.last_name")

    class Meta:
        model = Doctor
        fields = [
            "id",
            "first_name",
            "last_name",
            "specialization",
            "degree",
            "biography",
            "avatar",
            "appointment_gap",
            "medical_system_number",
            "appointment_fee",
        ]


class DoctorCreateUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(validators=[validators.validate_image_jpg_jpeg])

    class Meta:
        model = Doctor
        fields = [
            "specialization",
            "degree",
            "biography",
            "avatar",
            "appointment_gap",
            "medical_system_number",
            "appointment_fee",
        ]

    def validate(self, attrs):
        user_id = self.context["user_id"]
        doctor_exists = Doctor.objects.filter(profile_id=user_id).exists()

        if not self.instance:
            if not Profile.objects.filter(user_id=user_id).exists():
                raise serializers.ValidationError(
                    "لطفا اول اطلاعات حساب کاربری خود را تکمیل کنید"
                )

            if doctor_exists:
                raise serializers.ValidationError(
                    "شما از قبل اطلاعات پزشگی خود را ثبت کرده اید"
                )

        return super().validate(attrs)


class AdminDoctorCreateUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(validators=[validators.validate_image_jpg_jpeg])

    class Meta:
        model = Doctor
        fields = [
            "profile",
            "specialization",
            "degree",
            "biography",
            "avatar",
            "appointment_gap",
            "medical_system_number",
            "appointment_fee",
        ]

    def validate(self, attrs):
        user_id = self.context["user_id"]
        profile = attrs.get("profile")

        if not self.instance:
            if not Profile.objects.filter(user_id=user_id).exists():
                raise serializers.ValidationError(
                    "کاربر هنوز پروفایل خودرا تکمیل نکرده است"
                )

            if Doctor.objects.filter(profile_id=profile.id).exists():
                raise serializers.ValidationError(
                    "این کاربر از قبل اطلاعات پزشگی خود را ثبت کرده است"
                )

        return super().validate(attrs)


class SpecializationSerializer(serializers.ModelSerializer):
    image = serializers.FileField(validators=[validators.validate_image_svg])

    class Meta:
        model = Specialization
        fields = ["id", "name", "image"]


class DoctorDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDegree
        fields = ["id", "degree"]
