# Generated by Django 3.2.8 on 2022-08-30 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loan', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userloan',
            name='loan_due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
