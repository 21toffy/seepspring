from decimal import *
from django.db import models
from accounts.models import (CustomUser, BankAccountDetails)
from common.models import BaseModel
from common import constants
import datetime
from django.utils import timezone

from common.utils import float_to_decimal



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
    active = models.BooleanField(default=False)

    def __str__(self):
        return ":Loan purpose" + str(self.purpose)







class SinglePromotion(BaseModel):
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    image_url = models.URLField(max_length=300, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return "single promotion" + str(self.title)





class Interest(BaseModel):
    interest_name = models.CharField(max_length=300, null=True, blank=True)
    vat = models.DecimalField(default=7.5, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    service_charge = models.DecimalField(default=5.0, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    interest = models.DecimalField(default=28.0, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    active = models.BooleanField(default=False)
    @property
    def aggregated_interest(self):
        return self.vat + self.service_charge + self.interest

    def __str__(self):
        return str(self.interest_name)

class LoanPageInformationSlider(BaseModel):
    number = models.IntegerField(default=1, null=True, blank=True)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)
    image_url = models.URLField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.interest.interest_name) + "Active Loan Information Slider" + "Number "+ str(self.number)


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
    loan_repayment_status = models.CharField(
                default=constants.ONGOING,
                choices=constants.LOAN_REPAYMENT_STATUS,
                max_length=225)
    loan_purpose = models.ForeignKey(LoanPurpose, on_delete=models.CASCADE, null=True)
    account_number = models.ForeignKey(BankAccountDetails, on_delete=models.CASCADE, null=True)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, null=True)
    loan_level = models.ForeignKey(LoanLevel, on_delete=models.CASCADE, null=True, blank=True)
    paid = models.BooleanField(default=False)
    late_payment = models.BooleanField(default=False)
    amount_requested = models.DecimalField(default=0.00, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    amount_disbursed = models.DecimalField(default=0.00, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)

    payment_confirmation_status = models.BooleanField(default=False)
    paid_ontime = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    loan_date = models.DateField(auto_now_add=True)
    loan_due_date = models.DateField(blank=True, null=True)
    loan_time = models.TimeField(auto_now_add=True)
    loan_due_time = models.TimeField(blank=True, null=True)
    load_default_status = models.BooleanField(default=False)
    number_of_default_days = models.IntegerField(default=0)
    amount_left = models.DecimalField(default=0.00, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    accumulated_amount = models.DecimalField(default=0.00, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    # last_accumulate_date = models.DateField(default=timezone.now().date())
    last_accumulate_date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return str(self.user) + " is owing? " #+ str(self.get_loan_default_details["eligible_to_collect_loan"])

    def save(self, *args, **kwargs):
        self.loan_date = timezone.now().date()
        if not self.id:
            self.loan_due_date = self.loan_date + datetime.timedelta(days=self.loan_level.days_tenure)
            percentage_taken = (self.interest.interest * self.amount_requested) / 100
            company_percentage = self.interest.vat + self.interest.service_charge + percentage_taken / 100
            self.amount_disbursed = self.amount_requested - company_percentage * 100
            # self.amount_left = self.amount_requested

        self.loan_due_date = self.loan_date + datetime.timedelta(days=self.loan_level.days_tenure)
        percentage_taken = (self.interest.interest * self.amount_requested) / 100
        company_percentage = self.interest.vat + self.interest.service_charge + percentage_taken / 100
        self.amount_disbursed = self.amount_requested - company_percentage * 100

        return super(UserLoan, self).save(*args, **kwargs)

    # def save(self, *args, **kwargs):
    #     self.loan_date = timezone.now().date()
    #     if not self.id:
    #         self.loan_due_date = self.loan_date + datetime.timedelta(days=self.loan_level.days_tenure)
    #         percentage_taken = (self.interest.interest * self.amount_requested) /100
    #         company_percentage = self.interest.vat + self.interest.service_charge + percentage_taken/100
    #         self.amount_disbursed = self.amount_requested - company_percentage * 100
    #         # self.amount_left = self.amount_requested
    #     self.loan_due_date = self.loan_date+datetime.timedelta(days = self.loan_level.days_tenure)
    #     percentage_taken = (self.interest.interest * self.amount_requested) /100
    #     company_percentage = self.interest.vat + self.interest.service_charge + percentage_taken/100
    #     self.amount_disbursed = self.amount_requested - company_percentage * 100
    #     return super(UserLoan, self).save(*args, **kwargs)


    @property
    def loan_purpose_name(self,):
        return self.loan_purpose.purpose
    @property
    def bank_account_number(self,):
        return self.account_number.account_number
    @property
    def bank_name(self,):
        return self.account_number.bank_name

    @property
    def interest_name(self,):
        return self.interest.interest_name
 
    # @property
    # def loan_level(self,):
    #     return self.loan_level.loan_name


    @property
    def service_charge(self,):
        return self.amount_requested - self.amount_disbursed
        


    @property
    def get_loan_default_details(self,):
        response_data = {}
        todays_date = datetime.date.today()
        if self.active and not self.paid:
            if  todays_date > self.loan_due_date:
                default_delta = todays_date - self.loan_due_date
                default_days = default_delta.days
                return {
                    "eligible_to_collect_loan": False,
                    "loan_date": self.loan_date,
                    "loan_due_date": self.loan_due_date,
                    "number_defaulted_days": default_days,
                    "details":"You have an overdue loan, please payback now to avoid a bad credit score"
                }
            else:
                return {
                    "eligible_to_collect_loan": False,
                    "loan_date": self.loan_date,
                    "loan_due_date": self.loan_due_date,
                    "details":"You have a running loan, please payback in other to qualify for another loan"

                }


        return {"eligible_to_collect_loan": True}


    # @property
    # def get_loan_default_details(self,):
    #     todays_date = datetime.date.today()
    #     if self.active and not self.paid and todays_date > self.loan_due_date:
    #         default_delta = todays_date - self.loan_due_date
    #         default_days = default_delta.days
    #         return {
    #             "eligible_to_collect_loan": False,
    #             "loan_date": self.loan_date,
    #             "loan_due_date": self.loan_due_date,
    #             "number_defaulted_days": default_days,
    #         }

    #     return {"eligible_to_collect_loan": True}

class LoanRepayment(BaseModel):
    user_loan = models.ForeignKey(UserLoan, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(default=0.00, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    repayment_date = models.DateTimeField(auto_now_add=True)
    transaction_refernce = models.CharField(max_length=255)
    editable_repayment_date = models.DateTimeField(auto_now=True)
    confirmation_status = models.BooleanField(default=False)

    @property
    def user_id(self,):
        return self.user_loan.id
    @property
    def loan_due_date(self,):
        return self.user_loan.loan_due_date
    @property
    def days_overdue(self,):
        return self.user_loan.number_of_default_days
    @property
    def amount_left(self,):
        return self.user_loan.amount_left + self.user_loan.accumulated_amount
    @property
    def loan_id(self,):
        return self.user_loan.id


class AmountDisbursed(BaseModel):
    user_loan = models.ForeignKey(UserLoan, on_delete=models.CASCADE, null=True)
    amount_disbursed = models.DecimalField(default=0.00, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    disbursement_date = models.DateTimeField(auto_now_add=True)
    transaction_refernce = models.CharField(max_length=255)
    editable_disbursement_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

    @property
    def user_id(self,):
        return self.user_loan.id
    @property
    def bank_name(self,):
        return self.user_loan.account_number.bank_name
    @property
    def account_number(self,):
        return self.user_loan.account_number.account_number