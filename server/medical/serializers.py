from rest_framework import serializers
from . import validators
from .models import Province, City


class ProvinceSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(validators=[validators.validate_image])

    class Meta:
        model = Province
        fields = ['id', 'name', 'image', 'slug', 'created']


class CityListRetrieveSerializer(serializers.ModelSerializer):
    province = serializers.CharField(source='province.name')

    class Meta:
        model = City
        fields = ['id', 'province', 'name', 'slug', 'created']

class CityCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['province', 'name', 'slug']


class ProvinceCitiesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'slug']

    