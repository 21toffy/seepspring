# Generated by Django 3.2.8 on 2022-08-15 18:21

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=14, unique=True, validators=[accounts.models.validate_mobile_num], verbose_name='phone number')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=100, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, unique=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=300, null=True)),
                ('bvn', models.CharField(blank=True, max_length=100, null=True)),
                ('education', models.CharField(blank=True, max_length=225, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=225, null=True)),
                ('current_addres', models.CharField(blank=True, max_length=225, null=True)),
                ('number_of_children', models.IntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('image', models.URLField(blank=True, max_length=250, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmploymentDuration',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1)),
                ('description', models.CharField(blank=True, max_length=225, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalaryRange',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1)),
                ('description', models.CharField(blank=True, max_length=225, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Employmentinformation',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('employment_status', models.CharField(blank=True, max_length=225, null=True)),
                ('company_name', models.CharField(blank=True, max_length=225, null=True)),
                ('company_location', models.CharField(blank=True, max_length=225, null=True)),
                ('role', models.CharField(blank=True, max_length=225, null=True)),
                ('employee_id_card', models.URLField(blank=True, max_length=250, null=True)),
                ('bank_statement', models.URLField(blank=True, max_length=250, null=True)),
                ('employment_duration', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.employmentduration')),
                ('salary_range', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.salaryrange')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('relationship', models.CharField(blank=True, max_length=225, null=True)),
                ('name', models.CharField(blank=True, max_length=225, null=True)),
                ('phone_number', models.CharField(max_length=14, validators=[accounts.models.validate_mobile_num], verbose_name='Emergency contact phone number')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ColleagueContact',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=225, null=True)),
                ('relationship', models.CharField(blank=True, default='colleague', max_length=225, null=True)),
                ('phone_number', models.CharField(max_length=14, validators=[accounts.models.validate_mobile_num], verbose_name='Emergency contact phone number')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BankAccountDetails',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('bank_name', models.CharField(blank=True, max_length=225, null=True)),
                ('account_number', models.CharField(blank=True, max_length=225, null=True)),
                ('account_name', models.CharField(blank=True, default='colleague', max_length=225, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]