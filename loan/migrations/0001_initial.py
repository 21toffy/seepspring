# Generated by Django 3.2.8 on 2023-03-24 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guarntee',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('text_1', models.CharField(blank=True, max_length=300, null=True)),
                ('text_2', models.CharField(blank=True, max_length=300, null=True)),
                ('text_3', models.CharField(blank=True, max_length=300, null=True)),
                ('text_4', models.CharField(blank=True, max_length=300, null=True)),
                ('text_5', models.CharField(blank=True, max_length=300, null=True)),
                ('text_6', models.CharField(blank=True, max_length=300, null=True)),
                ('text_7', models.CharField(blank=True, max_length=300, null=True)),
                ('text_8', models.CharField(blank=True, max_length=300, null=True)),
                ('text_9', models.CharField(blank=True, max_length=300, null=True)),
                ('text_10', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomePagePromotion',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('promotion_type', models.CharField(blank=True, max_length=300, null=True)),
                ('text_1', models.CharField(blank=True, max_length=300, null=True)),
                ('text_2', models.CharField(blank=True, max_length=300, null=True)),
                ('text_3', models.CharField(blank=True, max_length=300, null=True)),
                ('text_4', models.CharField(blank=True, max_length=300, null=True)),
                ('text_5', models.CharField(blank=True, max_length=300, null=True)),
                ('text_6', models.CharField(blank=True, max_length=300, null=True)),
                ('text_7', models.CharField(blank=True, max_length=300, null=True)),
                ('text_8', models.CharField(blank=True, max_length=300, null=True)),
                ('text_9', models.CharField(blank=True, max_length=300, null=True)),
                ('text_10', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Interest',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('interest_name', models.CharField(blank=True, max_length=300, null=True)),
                ('vat', models.DecimalField(decimal_places=2, default=7.5, max_digits=11)),
                ('service_charge', models.DecimalField(decimal_places=2, default=5.0, max_digits=11)),
                ('interest', models.DecimalField(decimal_places=2, default=28.0, max_digits=11)),
                ('active', models.BooleanField(default=False)),
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
                ('active', models.BooleanField(default=False)),
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
            name='LoanPurpose',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('purpose', models.CharField(blank=True, max_length=300, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RepaymentGuide',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('repayment_type', models.CharField(blank=True, max_length=300, null=True)),
                ('text_1', models.CharField(blank=True, max_length=300, null=True)),
                ('text_2', models.CharField(blank=True, max_length=300, null=True)),
                ('text_3', models.CharField(blank=True, max_length=300, null=True)),
                ('text_4', models.CharField(blank=True, max_length=300, null=True)),
                ('text_5', models.CharField(blank=True, max_length=300, null=True)),
                ('text_6', models.CharField(blank=True, max_length=300, null=True)),
                ('text_7', models.CharField(blank=True, max_length=300, null=True)),
                ('text_8', models.CharField(blank=True, max_length=300, null=True)),
                ('text_9', models.CharField(blank=True, max_length=300, null=True)),
                ('text_10', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SinglePromotion',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('image_url', models.URLField(blank=True, max_length=300, null=True)),
                ('active', models.BooleanField(default=False)),
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
                ('loan_request_status', models.CharField(choices=[('PENDING', 'PENDING'), ('DISBURSED', 'DISBURSED'), ('DISAPPROVED', 'DISAPPROVED')], default='PENDING', max_length=225)),
                ('loan_repayment_status', models.CharField(choices=[('LATE', 'LATE'), ('SETTLED', 'SETTLED'), ('PART SETTLEMENT', 'PART SETTLEMENT'), ('ONGOING', 'ONGOING')], default='ONGOING', max_length=225)),
                ('paid', models.BooleanField(default=False)),
                ('late_payment', models.BooleanField(default=False)),
                ('amount_requested', models.DecimalField(decimal_places=2, default=0.0, max_digits=11)),
                ('amount_disbursed', models.DecimalField(decimal_places=2, default=0.0, max_digits=11)),
                ('payment_confirmation_status', models.BooleanField(default=False)),
                ('paid_ontime', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('loan_date', models.DateField(auto_now_add=True)),
                ('loan_due_date', models.DateField(blank=True, null=True)),
                ('loan_time', models.TimeField(auto_now_add=True)),
                ('loan_due_time', models.TimeField(blank=True, null=True)),
                ('load_default_status', models.BooleanField(default=False)),
                ('number_of_default_days', models.IntegerField(default=0)),
                ('amount_left', models.DecimalField(decimal_places=2, default=0.0, max_digits=11)),
                ('accumulated_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=11)),
                ('last_accumulate_date', models.DateField(default=django.utils.timezone.now)),
                ('account_number', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.bankaccountdetails')),
                ('interest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.interest')),
                ('loan_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.loanlevel')),
                ('loan_purpose', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.loanpurpose')),
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
                ('active', models.BooleanField(default=False)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=11)),
                ('repayment_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_refernce', models.CharField(max_length=255)),
                ('editable_repayment_date', models.DateTimeField(auto_now=True)),
                ('confirmation_status', models.BooleanField(default=False)),
                ('user_loan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.userloan')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LoanPageInformationSlider',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('number', models.IntegerField(blank=True, default=1, null=True)),
                ('title', models.CharField(blank=True, max_length=300, null=True)),
                ('description', models.CharField(blank=True, max_length=300, null=True)),
                ('image_url', models.URLField(blank=True, max_length=300, null=True)),
                ('interest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.interest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='InterestBreakdown',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('text_1', models.CharField(blank=True, max_length=300, null=True)),
                ('text_2', models.CharField(blank=True, max_length=300, null=True)),
                ('text_4', models.CharField(blank=True, max_length=300, null=True)),
                ('text_5', models.CharField(blank=True, max_length=300, null=True)),
                ('text_6', models.CharField(blank=True, max_length=300, null=True)),
                ('text_7', models.CharField(blank=True, max_length=300, null=True)),
                ('text_8', models.CharField(blank=True, max_length=300, null=True)),
                ('text_9', models.CharField(blank=True, max_length=300, null=True)),
                ('text_10', models.CharField(blank=True, max_length=300, null=True)),
                ('interest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.interest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AmountDisbursed',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=False)),
                ('amount_disbursed', models.DecimalField(decimal_places=2, default=0.0, max_digits=11)),
                ('disbursement_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_refernce', models.CharField(max_length=255)),
                ('editable_disbursement_date', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=False)),
                ('user_loan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='loan.userloan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
