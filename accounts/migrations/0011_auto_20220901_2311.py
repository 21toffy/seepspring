# Generated by Django 3.2.8 on 2022-09-01 22:11

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20220831_0255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='current_addres',
            new_name='current_address',
        ),
        migrations.AddField(
            model_name='customuser',
            name='address_image_url',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='bvn_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='bvn_phone_number',
            field=models.CharField(max_length=14, null=True, unique=True, validators=[accounts.models.validate_mobile_num], verbose_name='phone number'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='lga_of_origin',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='state_of_origin',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
