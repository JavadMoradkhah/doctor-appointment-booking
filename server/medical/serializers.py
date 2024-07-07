from rest_framework import serializers
from . import validators
from .models import Province, City, Insurance, UserInsurance


class ProvinceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validators.validate_image])

    class Meta:
        model = Province
        fields = ['id', 'name', 'image', 'slug']


class CityListRetrieveSerializer(serializers.ModelSerializer):
    province = serializers.CharField(source='province.name')

    class Meta:
        model = City
        fields = ['id', 'name', 'slug', 'province']


class CityCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['province', 'name', 'slug']


class ProvinceCitiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'slug']


class InsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Insurance
        fields = ['id', 'name']


class UserInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInsurance
        fields = ['id', 'insurance', 'insurance_code']

    def create(self, validated_data):
        validated_data['user_id'] = self.context['user_id']
        return UserInsurance.objects.create(**validated_data)
