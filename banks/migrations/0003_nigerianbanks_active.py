# Generated by Django 3.2.8 on 2022-08-31 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0002_rename_employmentduration_nigerianbanks'),
    ]

    operations = [
        migrations.AddField(
            model_name='nigerianbanks',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
