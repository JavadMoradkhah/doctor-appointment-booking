from django.contrib import admin
from . import models
# Register your models here.


@admin.register(models.Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)



@admin.register(models.City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.UserInsurance)
class UserInsuranceAdmin(admin.ModelAdmin):
    list_display = ('insurance_code',)
