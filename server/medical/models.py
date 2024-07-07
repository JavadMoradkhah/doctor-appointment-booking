from django.db import models
from . import validators
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class Province(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(
        upload_to='province/images/', validators=[validators.validate_image])
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Insurance(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class UserInsurance(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_insurances')
    insurance = models.ForeignKey(
        Insurance, on_delete=models.PROTECT, related_name='user_insurances')
    insurance_code = models.CharField(max_length=50, unique=True)

    class Meta:
        unique_together = ['user', 'insurance_code']

    def __str__(self):
        return self.insurance_code
