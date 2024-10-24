from django.db import transaction
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from account.models import Profile
from .models import (
    Province,
    City,
    Insurance,
    UserInsurance,
    Facility,
    MedicalCenter,
    MedicalCenterStatus,
    MedicalCenterGallery,
    MedicalCenterAddress,
    MedicalCenterSchedule,
    MedicalCenterTelephone,
)
from . import validators, choices
from .utils import calc_time_diff


class ProvinceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name", "slug"]


class ProvinceRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name", "slug", "image"]


class ProvinceCreateUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validators.validate_image])

    class Meta:
        model = Province
        fields = ["name", "image", "slug"]


class CityListRetrieveSerializer(serializers.ModelSerializer):
    province = serializers.CharField(source="province.name")

    class Meta:
        model = City
        fields = ["id", "name", "slug", "province"]


class CityCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["province", "name", "slug"]


class ProvinceCitiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "slug"]


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = ["id", "name"]


class UserInsuranceListRetrieveSerializer(serializers.ModelSerializer):
    insurance = serializers.CharField(source="insurance.name")

    class Meta:
        model = UserInsurance
        fields = ["id", "insurance", "insurance_code"]


class UserInsuranceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInsurance
        fields = ["id", "insurance", "insurance_code"]

    def validate(self, attrs):
        user_id = self.context["user_id"]

        if UserInsurance.objects.filter(user_id=user_id).count() >= 2:
            raise ValidationError("امکان ثبت بیشتراز 2 بیمه وجود ندارد")

        return super().validate(attrs)

    def create(self, validated_data):
        user_id = self.context["user_id"]
        return UserInsurance.objects.create(**validated_data, user_id=user_id)


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["id", "name", "slug"]


class MedicalCenterManagerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="user.phone")

    class Meta:
        model = Profile
        fields = ["user", "first_name", "last_name", "phone", "avatar"]


class MedicalCenterCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "slug"]


class MedicalCenterStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterStatus
        fields = ["approval_status", "description"]


class MedicalCenterListSerializer(serializers.ModelSerializer):
    facility = serializers.CharField(source="facility.name")
    city = serializers.CharField(source="city.name")

    class Meta:
        model = MedicalCenter
        exclude = ["introduction", "manager"]


class AdminMedicalCenterListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="status.approval_status")
    facility = serializers.CharField(source="facility.name")
    city = serializers.CharField(source="city.name")

    class Meta:
        model = MedicalCenter
        exclude = ["introduction", "manager"]


class MedicalCenterGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterGallery
        fields = ["id", "photo", "caption"]
        extra_kwargs = {"photo": {"validators": [validators.validate_image]}}

    def validate(self, attrs):
        medical_center_id = self.context["medical_center_id"]

        gallery_count = MedicalCenterGallery.objects.filter(
            medical_center_id=medical_center_id
        ).count()

        if gallery_count >= 6:
            raise ValidationError("حداکثر ۶ تصویر برای گالری مراکز درمانی مجاز می باشد")

        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        medical_center_id = self.context["medical_center_id"]
        validated_data["medical_center_id"] = medical_center_id

        gallery = super().create(validated_data)

        MedicalCenterStatus.objects.filter(medical_center_id=medical_center_id).update(
            approval_status=choices.MEDICAL_CENTER_STATUS_PENDING
        )

        return gallery


class MedicalCenterTelephoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterTelephone
        fields = ["id", "telephone", "description"]
        extra_kwargs = {"telephone": {"validators": [validators.TelephoneValidator()]}}

    def validate(self, attrs):
        telephone = attrs["telephone"]
        medical_center_id = self.context["medical_center_id"]

        gallery_count = MedicalCenterTelephone.objects.filter(
            medical_center_id=medical_center_id
        ).count()

        if gallery_count >= 3:
            raise ValidationError("حداکثر ۳ شماره تلفن برای مراکز درمانی مجاز می باشد")

        telephone_exists = MedicalCenterTelephone.objects.filter(
            medical_center_id=medical_center_id, telephone=telephone
        ).exists()

        if telephone_exists:
            raise ValidationError("این شماره تلفن قبلا اضافه شده است")

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["medical_center_id"] = self.context["medical_center_id"]
        return super().create(validated_data)


class MedicalCenterAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterAddress
        fields = ["id", "area", "address"]

    @transaction.atomic()
    def save(self, **kwargs):
        medical_center_id = self.context["medical_center_id"]
        self.validated_data["medical_center_id"] = medical_center_id

        address = super().save(**kwargs)

        MedicalCenterStatus.objects.filter(medical_center_id=medical_center_id).update(
            approval_status=choices.MEDICAL_CENTER_STATUS_PENDING
        )

        return address


class MedicalCenterScheduleSerializer(serializers.ModelSerializer):
    day_name = serializers.SerializerMethodField(method_name="get_day_name")

    def get_day_name(self, schedule):
        return schedule.get_day_display()

    class Meta:
        model = MedicalCenterSchedule
        fields = ["id", "day", "day_name", "open_at", "close_at"]

    def validate(self, attrs):
        day = attrs["day"]
        open_at = attrs["open_at"]
        close_at = attrs["close_at"]
        medical_center_id = self.context["medical_center_id"]

        if not self.instance:
            exists = MedicalCenterSchedule.objects.filter(
                medical_center_id=medical_center_id, day=day
            )

            if exists:
                raise ValidationError("این روز کاری قبلا اضافه شده است")

        times_diff = calc_time_diff(close_at, open_at)

        if times_diff < 3600:
            raise ValidationError("روز کاری مراکز درمانی نباید کمتر از یک ساعت باشد")

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["medical_center_id"] = self.context["medical_center_id"]
        return super().create(validated_data)


class MedicalCenterRetrieveSerializer(serializers.ModelSerializer):
    facility = serializers.CharField(source="facility.name")
    city = serializers.CharField(source="city.name")
    gallery = MedicalCenterGallerySerializer(many=True)
    telephones = MedicalCenterTelephoneSerializer(many=True)
    address = MedicalCenterAddressSerializer()

    class Meta:
        model = MedicalCenter
        exclude = ["manager"]


class AdminMedicalCenterRetrieveSerializer(serializers.ModelSerializer):
    manager = MedicalCenterManagerSerializer(source="manager.profile")
    facility = FacilitySerializer()
    city = MedicalCenterCitySerializer()
    status = MedicalCenterStatusSerializer()
    gallery = MedicalCenterGallerySerializer(many=True)
    telephones = MedicalCenterTelephoneSerializer(many=True)
    address = MedicalCenterAddressSerializer()

    class Meta:
        model = MedicalCenter
        fields = [
            "id",
            "status",
            "manager",
            "facility",
            "city",
            "name",
            "slug",
            "introduction",
            "photo",
        ]


class MedicalCenterCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenter
        fields = [
            "facility",
            "city",
            "name",
            "introduction",
            "photo",
        ]

    def validate(self, attrs):
        if not self.instance:
            user_id = self.context["user_id"]
            profile_exists = Profile.objects.filter(user_id=user_id).exists()

            if not profile_exists:
                raise ValidationError(
                    "برای ثبت مرکز درمانی ابتدا باید حساب کاربری خود را تکمیل کنید"
                )

        return super().validate(attrs)

    @transaction.atomic()
    def create(self, validated_data):
        validated_data["manager_id"] = self.context["user_id"]
        validated_data["slug"] = slugify(validated_data["name"], allow_unicode=True)
        medical_center = super().create(validated_data)
        MedicalCenterStatus.objects.create(medical_center_id=medical_center.id)
        return medical_center

    @transaction.atomic()
    def update(self, instance, validated_data):
        if "name" in validated_data:
            validated_data["slug"] = slugify(validated_data["name"], allow_unicode=True)

        medical_center = super().update(instance, validated_data)

        MedicalCenterStatus.objects.filter(medical_center_id=medical_center.id).update(
            approval_status=choices.MEDICAL_CENTER_STATUS_PENDING
        )

        return medical_center


class MedicalCenterStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenterStatus
        fields = ["approval_status", "description"]
