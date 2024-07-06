from django.core.exceptions import ValidationError
import pathlib


def validate_image(image):
    extensions = pathlib.Path(image.name).suffix
    allow_extensions = ['.jpg', '.jpeg']
    if not extensions in allow_extensions:
        raise ValidationError(f'({allow_extensions})فرمت ارسال شده معتبر نمی باشد فرمت های مجاز')
    if image.size > 2 * 1024 **2:
        raise ValidationError(f'سایز تصویر مجاز نمی باشد  سایز مجاز 2 مگابایت می باشد')