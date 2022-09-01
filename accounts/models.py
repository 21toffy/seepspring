from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import BaseModel
# from loan.models import UserLoan
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from common import constants
from django.db.models import Q


from .managers import CustomUserManager


from django.core.exceptions import ValidationError


def validate_mobile_num(value):
    valid_starters = ["080", "070", "090", "081"]
    if len(str(value)) != 11 or [i.isalpha() for i in str(value) if i.isalpha()]:
        raise ValidationError(
            _("%(value)s is not a valid Phone number"),
            params={"value": value},
        )


class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    choice_gender = (                          #private attributes
          ('Male', 'Male'),
          ('Female', 'Female'),         
    )
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), unique=True, max_length=14, validators=[validate_mobile_num])
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    middle_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=choice_gender)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=300, null=True, blank=True)
    lga_of_origin = models.CharField(max_length=300, null=True, blank=True)
    state_of_origin = models.CharField(max_length=300, null=True, blank=True)

    bvn = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=225, null=True, blank=True)
    marital_status = models.CharField(max_length=225, null=True, blank=True)
    current_address = models.CharField(max_length=225, null=True, blank=True)
    number_of_children = models.CharField(max_length=225, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    bvn_phone_number = models.CharField(_('phone number'), unique=True, max_length=14, validators=[validate_mobile_num], null=True)
    bvn_address = models.CharField(max_length=255, null=True, blank=True)
    address_image_url = models.URLField(max_length=255, null=True, blank=True)





    user_level = models.IntegerField(
                editable=False,
                default=constants.LEVEL_1,
                choices=constants.LEVEL_CHOICES)
    image = models.URLField(max_length=250, null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    # @property
    # def get_loan_eligibility(self,):
    #     UserLoan.objects.filter(
    #         # (user=self.id) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.DISBURSED) |
    #         # Q(loan_request_status=constants.LATE) |
    #         # Q(loan_request_status=constants.PART_SETTLEMENT) |
    #         Q(paid=False) |
    #         Q(active=False) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         # Q(loan_request_status=constants.PENDING) |
    #         )
    #     return 200

    @property
    def full_name(self):
        return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)
    
    @property
    def my_email(self):
        return "{}".format(self.email)


    def __str__(self):
        return str(self.full_name)

    @property
    def user_id(self):
        return self.id.__str__()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class EmploymentDuration(BaseModel):
    level =  models.IntegerField(default=1)
    description = models.CharField(max_length=225, null=True, blank=True)
    def __str__(self):
        return self.description + " ::::Level " + str(self.level)



class SalaryRange(BaseModel):
    level =  models.IntegerField(default=1)
    description = models.CharField(max_length=225, null=True, blank=True)

    def __str__(self):
        return self.description + " ::::Level " + str(self.level)




class UserEmploymentDuration(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    employment_duration = models.ForeignKey(EmploymentDuration, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user) + " :::: " + str(self.employment_duration)


class UserSalaryRange(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    salary_range = models.ForeignKey(SalaryRange, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user) + " :::: " + str(self.salary_range)



class Employmentinformation(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    employment_status = models.CharField(max_length=225, null=True, blank=True)
    company_name = models.CharField(max_length=225, null=True, blank=True)
    company_location = models.CharField(max_length=225, null=True, blank=True)
    role = models.CharField(max_length=225, null=True, blank=True)
    employee_id_card = models.URLField(max_length = 250, null=True, blank = True)
    bank_statement = models.URLField(max_length = 250, null=True, blank = True)
    
    employment_duration = models.ForeignKey(EmploymentDuration, on_delete=models.CASCADE, null=True)
    salary_range = models.ForeignKey(SalaryRange, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.user) + f": {str(self.employment_status)} {str(self.company_name)} {str(self.role)} {str(self.salary_range)}"


class EmergencyContact(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=225, null=True, blank=True)
    name = models.CharField(max_length=225, null=True, blank=True)
    phone_number = models.CharField(_('Emergency contact phone number'), max_length=14, validators=[validate_mobile_num], null=True, blank=True)


class ColleagueContact(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=225, null=True, blank=True)
    relationship = models.CharField(max_length=225, null=True, blank=True, default="colleague")
    phone_number = models.CharField(_('Emergency contact phone number'), max_length=14, validators=[validate_mobile_num], null=True, blank=True)



class BankAccountDetails(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=225, null=True, blank=True)
    account_number = models.CharField(max_length=225, null=True, blank=True)
    account_name = models.CharField(max_length=225, null=True, blank=True, default="colleague")

