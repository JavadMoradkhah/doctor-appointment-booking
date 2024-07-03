from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .validators import PhoneValidator
from .managers import UserManager
from . import choices


class User(AbstractBaseUser):
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[PhoneValidator()]
    )
    role = models.CharField(
        max_length=10,
        choices=choices.USER_ROLE_CHOICES,
        default=choices.USER_ROLE_PATIENT
    )
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return self.phone

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    @property
    def is_staff(self):
        return self.role == choices.USER_ROLE_ADMIN

    @property
    def is_doctor(self):
        return self.role == choices.USER_ROLE_DOCTOR

    @property
    def is_patient(self):
        return self.role == choices.USER_ROLE_PATIENT


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    nation_code = models.CharField(max_length=10, unique=True)
    gender = models.CharField(
        max_length=10,
        choices=choices.USER_GENDER_CHOICES
    )
    date_of_birth = models.DateField()
