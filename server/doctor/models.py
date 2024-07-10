from django.db import models
from account.models import Profile
from . import validators

# Create your models here.


class Specialization(models.Model):
    name = models.CharField(
        max_length=50,
    )
    image = models.FileField(
        upload_to="specialization/images", validators=[validators.validate_image_svg]
    )

    def __str__(self) -> str:
        return self.name


class DoctorDegree(models.Model):
    degree = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.degree


class Doctor(models.Model):
    profile = models.OneToOneField(
        Profile, on_delete=models.CASCADE, related_name="doctor"
    )
    specialization = models.ForeignKey(
        Specialization, on_delete=models.PROTECT, related_name="doctor"
    )
    degree = models.ForeignKey(
        DoctorDegree, on_delete=models.PROTECT, related_name="doctor"
    )
    biography = models.TextField(null=True, blank=True)
    avatar = models.ImageField(
        upload_to="doctor/avatars",
        null=True,
        blank=True,
        validators=[validators.validate_image_jpg_jpeg],
    )
    appointment_gap = models.DurationField()
    medical_system_number = models.CharField(max_length=10)
    appointment_fee = models.IntegerField()

    def __str__(self) -> str:
        return self.name
