from rest_framework import serializers
from . import validators
from .models import Province, City


class ProvinceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validators.validate_image])

    class Meta:
        model = Province
        fields = ['id', 'name', 'image', 'slug', 'created']


class CitySerializer(serializers.ModelSerializer):
    province = serializers.StringRelatedField()

    class Meta:
        model = City
        fields = ['id', 'province', 'name', 'slug', 'created']


class ProvinceCitiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'slug']

    