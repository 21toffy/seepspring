from django.db import models
from accounts.models import CustomUser
from common.models import BaseModel
from common import constants
import datetime
from django.utils import timezone



class HomePagePromotion(BaseModel):
    promotion_type = models.CharField(max_length=300, null=True, blank=True)
    text_1 = models.CharField(max_length=300, null=True, blank=True)
    text_2 = models.CharField(max_length=300, null=True, blank=True)
    text_3 = models.CharField(max_length=300, null=True, blank=True)
    text_4 = models.CharField(max_length=300, null=True, blank=True)
    text_5 = models.CharField(max_length=300, null=True, blank=True)
    text_6 = models.CharField(max_length=300, null=True, blank=True)
    text_7 = models.CharField(max_length=300, null=True, blank=True)
    text_8 = models.CharField(max_length=300, null=True, blank=True)
    text_9 = models.CharField(max_length=300, null=True, blank=True)
    text_10 = models.CharField(max_length=300, null=True, blank=True)


class RepaymentGuide(BaseModel):
    repayment_type =  models.CharField(max_length=300, null=True, blank=True)
    text_1 = models.CharField(max_length=300, null=True, blank=True)
    text_2 = models.CharField(max_length=300, null=True, blank=True)
    text_3 = models.CharField(max_length=300, null=True, blank=True)
    text_4 = models.CharField(max_length=300, null=True, blank=True)
    text_5 = models.CharField(max_length=300, null=True, blank=True)
    text_6 = models.CharField(max_length=300, null=True, blank=True)
    text_7 = models.CharField(max_length=300, null=True, blank=True)
    text_8 = models.CharField(max_length=300, null=True, blank=True)
    text_9 = models.CharField(max_length=300, null=True, blank=True)
    text_10 = models.CharField(max_length=300, null=True, blank=True)
    





class Guarntee(BaseModel):
    text_1 = models.CharField(max_length=300, null=True, blank=True)
    text_2 = models.CharField(max_length=300, null=True, blank=True)
    text_3 = models.CharField(max_length=300, null=True, blank=True)
    text_4 = models.CharField(max_length=300, null=True, blank=True)
    text_5 = models.CharField(max_length=300, null=True, blank=True)
    text_6 = models.CharField(max_length=300, null=True, blank=True)
    text_7 = models.CharField(max_length=300, null=True, blank=True)
    text_8 = models.CharField(max_length=300, null=True, blank=True)
    text_9 = models.CharField(max_length=300, null=True, blank=True)
    text_10 = models.CharField(max_length=300, null=True, blank=True)



class LoanPurpose(BaseModel):
    purpose = models.CharField(max_length=300, null=True, blank=True)



class Interest(BaseModel):
    interest_name = models.CharField(max_length=300, null=True, blank=True)
    vat = models.DecimalField(default=7.5, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    service_charge = models.DecimalField(default=5.0, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    interest = models.DecimalField(default=28.0, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    active = models.BooleanField(default=False)
    def __str__(self):
        return str(self.interest_name)


class InterestBreakdown(BaseModel):
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    text_1 = models.CharField(max_length=300, null=True, blank=True)
    text_2 = models.CharField(max_length=300, null=True, blank=True)
    text_4 = models.CharField(max_length=300, null=True, blank=True)
    text_5 = models.CharField(max_length=300, null=True, blank=True)
    text_6 = models.CharField(max_length=300, null=True, blank=True)
    text_7 = models.CharField(max_length=300, null=True, blank=True)
    text_8 = models.CharField(max_length=300, null=True, blank=True)
    text_9 = models.CharField(max_length=300, null=True, blank=True)
    text_10 = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.interest.interest_name) + " interest breakdown"



class LoanLevel(BaseModel):
    level = models.IntegerField(default=constants.LEVEL_1)
    loan_name = models.CharField(max_length=300, null=True, blank=True)
    max_amount = models.IntegerField(default=50000)
    min_amount = models.IntegerField(default=0)
    cycle = models.IntegerField(default=0)
    days_tenure = models.IntegerField(default=0)
    def __str__(self):
        return str(self.loan_name)

   
class UserLoan(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    loan_request_status = models.CharField(
                default=constants.PENDING,
                choices=constants.LOAN_REQUEST_STATUS,
                max_length=225)
    loan_purpose = models.ForeignKey(LoanPurpose, on_delete=models.CASCADE, null=True)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, null=True)
    loan_level = models.ForeignKey(LoanLevel, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    amount_requested = models.DecimalField(default=0.0, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    amount_disbursed = models.DecimalField(default=0.0, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)

    payment_confirmation_status = models.BooleanField(default=False)
    paid_ontime = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    loan_date = models.DateField(auto_now_add=True)
    loan_due_date = models.DateField(blank=True, null=True)

    loan_time = models.TimeField(auto_now_add=True)
    loan_due_time = models.TimeField(blank=True, null=True)

    load_default_status = models.BooleanField(default=False)
    number_of_default_days = models.IntegerField(default=0)
    amount_left = models.DecimalField(default=0.0, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    def __str__(self):
        return str(self.user) + " is owing? " + str(self.get_loan_default_details["eligible_to_collect_loan"])

    def save(self, *args, **kwargs):
        print(self.id,333333)
        if not self.id:
            print(1)
            self.loan_date = timezone.now()
            print(2)
            # self.loan_due_date = timezone.now().date()self.loan_date + datetime.timedelta(days=self.loan_level.days_tenure)

            self.loan_due_date = self.loan_date + datetime.timedelta(days=self.loan_level.days_tenure)
            print(3)
            company_percentage = self.amount_disbursed = self.interest.vat + self.interest.service_charge + self.interest.interest
            print(4)
            self.amount_disbursed = self.amount_requested - (company_percentage * self.amount_requested)/ 100
            print(5)

        # self.loan_due_date = timezone.now().date() + datetime.timedelta(days=self.loan_level.days_tenure)
        self.loan_due_date = self.loan_date  + datetime.timedelta(days=self.loan_level.days_tenure)

        company_percentage = self.amount_disbursed = self.interest.vat + self.interest.service_charge + self.interest.interest
        self.amount_disbursed = self.amount_requested - (company_percentage * self.amount_requested)/ 100
        print(44444444444444)
        return super(UserLoan, self).save(*args, **kwargs)

    @property
    def get_loan_default_details(self,):
        todays_date = datetime.date.today()
        if self.active and self.paid and todays_date > self.loan_due_date:
            default_delta = todays_date - self.loan_due_date
            default_days = default_delta.days
            return {
                "eligible_to_collect_loan": False,
                "loan_date": self.loan_date,
                "loan_due_date": self.loan_due_date,
                "number_defaulted_days": default_days,
            }

        return {"eligible_to_collect_loan": True}


class LoanRepayment(BaseModel):
    user_loan = models.ForeignKey(UserLoan, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(default=0.0, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    repayment_date = models.DateTimeField(auto_now_add=True)
    transaction_refernce = models.CharField(max_length=255)
    repayment_date = models.DateTimeField(auto_now_add=True)
    confirmation_status = models.BooleanField(default=False)


# class LoanDefault(BaseModel):
#     user_loan = models.ForeignKey(UserLoan, on_delete=models.CASCADE, null=True)
#     number_of
