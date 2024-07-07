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


@admin.register(models.Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(models.MedicalCenter)
class MedicalCenterAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(models.MedicalCenterSchedule)
class MedicalCenterScheduleAdmin(admin.ModelAdmin):
    list_display = ('medical_center', 'day', 'open_at', 'close_at')
