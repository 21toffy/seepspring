# Generated by Django 3.2.8 on 2022-12-18 22:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0015_alter_userloan_last_accumulate_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userloan',
            name='last_accumulate_date',
            field=models.DateField(default=datetime.date(2022, 12, 18)),
        ),
    ]