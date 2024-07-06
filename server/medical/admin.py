from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)