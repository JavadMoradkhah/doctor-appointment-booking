from django.db import models
from account.validators import PhoneValidator


class Otp(models.Model):
    phone = models.CharField(
        max_length=11,
        unique=True,
        validators=[PhoneValidator()],
        verbose_name="شماره موبایل"
    )
    code = models.CharField(max_length=255)
    attempts = models.PositiveSmallIntegerField(default=1)
    first_attempt = models.DateTimeField(auto_now_add=True)
    last_attempt = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    class Meta:
        indexes = [
            models.Index(fields=['phone'])
        ]

    def __str__(self) -> str:
        return f"Phone: {self.phone}"


class OtpBlacklist(models.Model):
    phone = models.CharField(
        max_length=11,
        validators=[PhoneValidator()],
        verbose_name="شماره موبایل"
    )
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['phone'])
        ]

    def __str__(self) -> str:
        return f"Blacklisted Phone: {self.phone}"
