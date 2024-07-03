from django.core.validators import RegexValidator


class PhoneValidator(RegexValidator):
    regex = r'^09([0-9]{9})$'
    message = 'یک شماره موبایل معتبر وارد کنید'
