# Generated by Django 4.2.13 on 2024-07-07 14:00

import account.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'کاربران'},
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال'),
        ),
        migrations.AlterField(
            model_name='user',
            name='joined_at',
            field=models.DateTimeField(
                auto_now_add=True, verbose_name='تاریخ عضویت'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, unique=True, validators=[
                                   account.validators.PhoneValidator()], verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'مدیر'), ('doctor', 'دکتر'), (
                'patient', 'بیمار')], default='patient', max_length=10, verbose_name='نقش'),
        ),
    ]
