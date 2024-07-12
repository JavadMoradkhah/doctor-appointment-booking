import pathlib
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class TelephoneValidator(RegexValidator):
    regex = r"^0([0-9]{10})$"
    message = "یک شماره تلفن معتبر وارد کنید"


def validate_image(image):
    extensions = pathlib.Path(image.name).suffix
    allow_extensions = [".jpg", ".jpeg"]

    if not extensions in allow_extensions:
        raise ValidationError(f"مجاز هستند {' و '.join(allow_extensions)} فقط فرمت های")

    if image.size > 2 * 1024 * 1024:
        raise ValidationError(f"حجم تصویر نباید بیش از ۲ مگابایت باشد")
