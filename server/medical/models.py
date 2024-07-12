from django.db import models
from django.contrib.auth import get_user_model
from .validators import TelephoneValidator
from . import validators, choices

User = get_user_model()


class Province(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    image = models.ImageField(
        upload_to="uploads/medical/images", validators=[validators.validate_image]
    )

    def __str__(self) -> str:
        return self.name


class City(models.Model):
    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, related_name="cities"
    )
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self) -> str:
        return self.name


class Insurance(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class UserInsurance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="insurances")
    insurance = models.ForeignKey(
        Insurance, on_delete=models.PROTECT, related_name="insurances"
    )
    insurance_code = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.insurance_code


class Facility(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    def __str__(self) -> str:
        return self.name


class MedicalCenter(models.Model):
    manager = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="medical_centers"
    )
    facility = models.ForeignKey(
        Facility, on_delete=models.PROTECT, related_name="medical_centers"
    )
    city = models.ForeignKey(
        City, on_delete=models.PROTECT, related_name="medical_centers"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    introduction = models.TextField(max_length=500)
    photo = models.ImageField(upload_to="uploads/medical/images", null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class MedicalCenterStatus(models.Model):
    medical_center = models.OneToOneField(
        MedicalCenter, primary_key=True, on_delete=models.CASCADE, related_name="status"
    )
    approval_status = models.CharField(
        max_length=20,
        choices=choices.MEDICAL_CENTER_STATUS_CHOICES,
        default=choices.MEDICAL_CENTER_STATUS_PENDING,
    )
    description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return self.get_approval_status_display()


class MedicalCenterTelephone(models.Model):
    medical_center = models.ForeignKey(
        MedicalCenter, on_delete=models.CASCADE, related_name="telephones"
    )
    telephone = models.CharField(max_length=11, validators=[TelephoneValidator()])
    description = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.telephone

    class Meta:
        unique_together = ["medical_center", "telephone"]


class MedicalCenterGallery(models.Model):
    medical_center = models.ForeignKey(
        MedicalCenter, on_delete=models.CASCADE, related_name="gallery"
    )
    photo = models.ImageField(upload_to="uploads/medical/images")
    caption = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.caption or "کپشن ندارد"


class MedicalCenterAddress(models.Model):
    medical_center = models.OneToOneField(
        MedicalCenter, on_delete=models.CASCADE, related_name="address"
    )
    area = models.CharField(max_length=100)
    address = models.TextField(max_length=500)

    def __str__(self) -> str:
        return self.address


class MedicalCenterSchedule(models.Model):
    medical_center = models.ForeignKey(
        MedicalCenter, on_delete=models.CASCADE, related_name="schedules"
    )
    day = models.PositiveSmallIntegerField(choices=choices.SCHEDULE_DAY_CHOICES)
    open_at = models.TimeField()
    close_at = models.TimeField()

    class Meta:
        unique_together = ["medical_center", "day"]

    def __str__(self) -> str:
        return f"{self.get_day_display()} از ساعت {self.open_at} تا {self.close_at}"
