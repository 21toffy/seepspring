# Generated by Django 3.2.8 on 2022-11-13 20:56

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_otpphone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpphone',
            name='phone',
            field=models.CharField(max_length=14, null=True, unique=True, validators=[accounts.models.validate_mobile_num], verbose_name='phone number'),
        ),
    ]
