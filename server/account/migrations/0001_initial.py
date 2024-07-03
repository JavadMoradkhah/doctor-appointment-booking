# Generated by Django 4.2.13 on 2024-07-03 16:56

import account.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('phone', models.CharField(max_length=11, unique=True, validators=[account.validators.PhoneValidator()])),
                ('role', models.CharField(choices=[('admin', 'مدیر'), ('doctor', 'دکتر'), ('patient', 'بیمار')], default='patient', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('nation_code', models.CharField(max_length=10, unique=True)),
                ('gender', models.CharField(choices=[('male', 'آقا'), ('female', 'خانم')], max_length=10)),
                ('date_of_birth', models.DateField()),
            ],
        ),
    ]
