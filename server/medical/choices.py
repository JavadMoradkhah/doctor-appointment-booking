MEDICAL_CENTER_STATUS_PENDING = "pending"
MEDICAL_CENTER_STATUS_APPROVED = "approved"
MEDICAL_CENTER_STATUS_SUSPENDED = "suspended"
MEDICAL_CENTER_STATUS_ARCHIVED = "archived"

MEDICAL_CENTER_STATUS_CHOICES = (
    (MEDICAL_CENTER_STATUS_PENDING, "در انتظار تایید"),
    (MEDICAL_CENTER_STATUS_APPROVED, "تایید شده"),
    (MEDICAL_CENTER_STATUS_SUSPENDED, "معلق شده"),
    (MEDICAL_CENTER_STATUS_ARCHIVED, "بایگانی شده"),
)

SCHEDULE_DAY_CHOICES = (
    (5, "شنبه"),
    (6, "یکشنبه"),
    (0, "دوشنبه"),
    (1, "سه‌شنبه"),
    (2, "چهارشنبه"),
    (3, "پنج‌شنبه"),
    (4, "جمعه"),
)
