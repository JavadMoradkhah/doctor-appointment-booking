import pathlib
from django.core.exceptions import ValidationError


def validate_image_jpg_jpeg(image):
    extensions = pathlib.Path(image.name).suffix
    allow_extensions = [".jpg", ".jpeg"]
    if not extensions in allow_extensions:
        raise ValidationError(
            f"{allow_extensions}فرمت ارسال شده معتبر نمی باشد فرمت های مجاز"
        )
    if image.size > 100 * 1024**2:
        raise ValidationError(f"سایز تصویر مجاز نمی باشد  سایز مجاز 2 مگابایت می باشد")


def validate_image_svg(image):
    extensions = pathlib.Path(image.name).suffix
    allow_extensions = [".svg"]
    if not extensions in allow_extensions:
        raise ValidationError(
            f"{allow_extensions}فرمت ارسال شده معتبر نمی باشد فرمت های مجاز"
        )
    if image.size > 400 * 1024:
        raise ValidationError(
            f"سایز تصویر مجاز نمی باشد  سایز مجاز 400 کیلو بایت باشد می باشد"
        )
