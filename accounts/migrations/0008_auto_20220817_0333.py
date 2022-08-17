# Generated by Django 3.2.8 on 2022-08-17 02:33

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_useremploymentduration_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colleaguecontact',
            name='phone_number',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[accounts.models.validate_mobile_num], verbose_name='Emergency contact phone number'),
        ),
        migrations.AlterField(
            model_name='emergencycontact',
            name='phone_number',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[accounts.models.validate_mobile_num], verbose_name='Emergency contact phone number'),
        ),
    ]
