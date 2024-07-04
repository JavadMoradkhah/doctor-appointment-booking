import os
from celery import Celery

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'doctor_appointment_booking.settings'
)

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    os.environ.get('DJANGO_SETTINGS_MODULE')
)

app = Celery('doctor_appointment_booking')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
