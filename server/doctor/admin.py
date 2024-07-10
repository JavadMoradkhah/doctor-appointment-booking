from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("appointment_gap",)


@admin.register(models.DoctorDegree)
class DoctorDegreeAdmin(admin.ModelAdmin):
    list_display = ("degree",)


@admin.register(models.Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ("name",)
