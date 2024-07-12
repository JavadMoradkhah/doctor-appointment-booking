from rest_framework import serializers
from medical.models import MedicalCenterSchedule
from account.models import Profile
from .models import Doctor, DoctorDegree, Specialization, DoctorSchedule
from . import validators


class DoctorListSerializer(serializers.ModelSerializer):
    specialization = serializers.CharField(source="specialization.name")
    degree = serializers.CharField(source="degree.degree")
    first_name = serializers.CharField(source="profile.first_name")
    last_name = serializers.CharField(source="profile.last_name")

    class Meta:
        model = Doctor
        fields = [
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
        extra_kwargs = {"avatar": {"validators": [validators.validate_image_jpg_jpeg]}}

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
        extra_kwargs = {"avatar": {"validators": [validators.validate_image_jpg_jpeg]}}

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
    # image = serializers.FileField(validators=[validators.validate_image_svg])

    class Meta:
        model = Specialization
        fields = ["id", "name", "image"]
        extra_kwargs = {"image": {"validators": [validators.validate_image_svg]}}


class DoctorDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorDegree
        fields = ["id", "degree"]


class DoctorScheduleListRetrieveSerializer(serializers.ModelSerializer):
    medical_center = serializers.CharField(source="medical_center.name")

    class Meta:
        model = DoctorSchedule
        fields = ["medical_center", "day", "start_at", "end_at"]


class DoctorScheduleCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = DoctorSchedule
        exclude = ["doctor"]

    def validate(self, attrs):
        day = attrs.get("day")
        medical_center_id = attrs.get("medical_center")
        start_at = attrs.get("start_at")
        end_at = attrs.get("end_at")

        if DoctorSchedule.objects.filter(
            doctor_id=self.context["user_id"],
            medical_center_id=medical_center_id,
            day=day,
        ).exists():
            raise serializers.ValidationError(
                "برای مرکز درمانی مورد نظر قبلا روز کاری ثبت کرده اید"
            )

        schedule = MedicalCenterSchedule.objects.filter(
            medical_center_id=medical_center_id, day=day
        ).first()

        if not schedule:
            raise serializers.ValidationError(
                "روز کاری انتخاب شده جزو روز کاری مرکز درمانی مورد نظر نیست"
            )

        if start_at < schedule.open_at or end_at > schedule.close_at:
            raise serializers.ValidationError(
                "زمان های انتخاب شده جزو ساعات کاری مرکز درمانی نمی باشد"
            )

        return super().validate(attrs)

    def create(self, validated_data):
        user_id = self.context["user_id"]
        return DoctorSchedule.objects.create(**validated_data, doctor_id=user_id)
