import os
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'doctor_appointment_booking.settings.development'
)

app = Celery('doctor_appointment_booking')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
