from django.db import models
from . import validators
# Create your models here.


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
