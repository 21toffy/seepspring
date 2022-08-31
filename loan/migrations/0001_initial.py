# Generated by Django 3.2.8 on 2022-08-30 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('interest_name', models.CharField(blank=True, max_length=300, null=True)),
                ('vat', models.DecimalField(decimal_places=2, default=7.5, max_digits=7)),
                ('service_charge', models.DecimalField(decimal_places=2, default=5.0, max_digits=7)),
                ('interest', models.DecimalField(decimal_places=2, default=28.0, max_digits=7)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoanLevel',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.IntegerField(default=1)),
                ('loan_name', models.CharField(blank=True, max_length=300, null=True)),
                ('max_amount', models.IntegerField(default=50000)),
                ('min_amount', models.IntegerField(default=0)),
                ('cycle', models.IntegerField(default=0)),
                ('days_tenure', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserLoan',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('paid', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('payment_confirmation_status', models.BooleanField(default=False)),
                ('paid_ontime', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('loan_date', models.DateTimeField(auto_now_add=True)),
                ('loan_due_date', models.DateTimeField()),
                ('load_default_status', models.BooleanField(default=False)),
                ('number_of_default_days', models.IntegerField(default=0)),
                ('amount_left', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('interest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.interest')),
                ('loan_level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.loanlevel')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoanRepayment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=7)),
                ('transaction_refernce', models.CharField(max_length=255)),
                ('repayment_date', models.DateTimeField(auto_now_add=True)),
                ('confirmation_status', models.BooleanField(default=False)),
                ('user_loan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.userloan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
