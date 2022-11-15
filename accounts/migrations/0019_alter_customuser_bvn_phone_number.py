# Generated by Django 3.2.8 on 2022-11-15 14:09

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_bvndata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='bvn_phone_number',
            field=models.CharField(max_length=14, null=True, unique=True, validators=[accounts.models.validate_mobile_num], verbose_name='BVN phone number'),
        ),
    ]
