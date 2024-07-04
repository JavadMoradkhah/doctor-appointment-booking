import requests
from django.conf import settings
from celery import shared_task


@shared_task
def send_otp(phone, otp):
    ENDPOINT = 'https://api.sms.ir/v1/send/verify/'

    headers = {
        'ACCEPT': 'application/json',
        'Content-Type': 'application/json',
        "X-API-KEY": settings.API_KEY_SMS,
    }

    data = {
        'Mobile': phone,
        'TemplateId': 784780,
        'Parameters': [
            {
                'Name': 'VERIFICATION_CODE',
                'Value': otp
            }
        ],
    }

    response = requests.post(ENDPOINT, headers=headers, json=data)

    response_data = response.json()

    if response_data['status'] != 1:
        raise Exception('Otp code was not sent!')
