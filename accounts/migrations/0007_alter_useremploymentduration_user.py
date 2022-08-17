# Generated by Django 3.2.8 on 2022-08-17 02:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_customuser_number_of_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useremploymentduration',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]