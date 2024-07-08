from rest_framework import serializers, status
from rest_framework.serializers import ValidationError
from .models import Province, City, Insurance, UserInsurance
from . import validators


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
