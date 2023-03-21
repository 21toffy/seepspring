from accounts.read_serializers import UserDetailsSerializer, UserRegistrationGetSerializer
from common import constants
from common.utils import unique_string
from accounts.models import (CustomUser)
from rest_framework import serializers

from loan.models import LoanLevel, UserLoan, LoanRepayment, AmountDisbursed
from loan.serializers import InterestSerializer

# serializers.py
from .models import Employee


from .models import Department, Role

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "department_name")

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "role_name")



class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['user', 'department', 'role', 'default_passsword']

    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        default_password = unique_string(6)
        validated_data['default_passsword'] = default_password

        employee_object = Employee.objects.create(**validated_data)
        return employee_object


class EmployeeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        extra_kwargs = {'password': {'write_only': True}}

        fields = [
            "email",
            "phone_number",        
            "first_name",
            "last_name",
        ]
    def create(self, validated_data):
        # create user 
        user = CustomUser.objects.create(
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            first_name = validated_data.get("first_name", "First name"),
            last_name = validated_data.get("last_name", "Last name"),
            role = validated_data.get("role", "reconciliation_officer"),

        )

        if user.password is not None:
            user.set_password(validated_data['phone_number'])
            user.save()
        
        return user


class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        exclude = ["user_loan", "editable_repayment_date"]


class UserLoanSerializer(serializers.ModelSerializer):


    loan_purpose_name = serializers.SerializerMethodField()
    bank_account_number = serializers.SerializerMethodField()
    bank_name = serializers.SerializerMethodField()

    interest_name = serializers.SerializerMethodField()
    # loan_level = serializers.SerializerMethodField()
    service_charge = serializers.SerializerMethodField()


    class Meta:
        model = UserLoan
        fields = [
            'loan_request_status',
            'loan_purpose_name',
            'bank_account_number', 
            'interest_name',
            # 'loan_level', 
            'bank_name',
            'paid',
            'late_payment', 
            'amount_requested',
            'amount_disbursed',
            'loan_date',
            'loan_due_date',
            'loan_time', 
            'number_of_default_days',
            'accumulated_amount', 
            'service_charge'
        ]
    def get_loan_purpose_name(self, obj):
        return obj.loan_purpose_name
    def get_bank_account_number(self, obj):
        return obj.bank_account_number
    def get_bank_name(self, obj):
        return obj.bank_name
    def get_interest_name(self, obj):
        return obj.interest_name
    # def get_loan_level(self, obj):
    #     return obj.loan_level
    def get_service_charge(self, obj):
        return obj.service_charge





class AmountDisbursedListSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    bank_name = serializers.SerializerMethodField()
    account_number = serializers.SerializerMethodField()


    class Meta:
        model = AmountDisbursed
        fields = ( 
            'id',
            'user_id',
            'amount_disbursed', 
            'bank_name',
            'account_number', 
            'disbursement_date',
            'status', 


            )
    def get_user_id(self, obj):
        return obj.user_id
    def get_bank_name(self, obj):
        return obj.bank_name
    def get_account_number(self, obj):
        return obj.account_number

            

class LoanRepaymentListSerializer(serializers.ModelSerializer):
    loan_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    loan_due_date = serializers.SerializerMethodField()
    days_overdue = serializers.SerializerMethodField()
    amount_left = serializers.SerializerMethodField()

    class Meta:
        model = LoanRepayment
        fields = ( 
            'id',
            'user_id',
            'amount', 
            'loan_due_date',
            'days_overdue', 
            'amount_left',
            'loan_id', 
            'transaction_refernce',
            'repayment_date', 

            )
    
    def get_loan_id(self, obj):
        return obj.loan_id
    def get_user_id(self, obj):
        return obj.user_loan.user.id
    def get_loan_due_date(self, obj):
        return obj.loan_due_date
    def get_days_overdue(self, obj):
        return obj.days_overdue
    def get_amount_left(self, obj):
        return obj.amount_left
    
    





class LoanApplicationListSerializer(serializers.ModelSerializer):
    service_charge = serializers.SerializerMethodField()
    class Meta:
        model = UserLoan
        fields = ( 'id', 'user', 'loan_date', 'amount_requested', 'amount_disbursed','service_charge', 'loan_request_status')
    
    def get_service_charge(self, obj):
        return obj.service_charge
    




class userListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ('pk', 'email', 'current_address', 'phone_number','full_name', 'status')
    def get_full_name(self, obj):
        return obj.full_name
    def get_status(self, obj):
        return "Active" if obj.is_active else "Inactive"

class DashboardUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [  "user_level",
                    "full_name",
                    "email",
                    "phone_number",
                    "dob","gender",
                    "state_of_origin",
                    "marital_status",
                    "current_address",
                    "bvn_phone_number",
                    "user_level",
        
        ]




class LoanLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanLevel
        fields = [
            "id", "level", "loan_name", "max_amount", "min_amount", "cycle", "days_tenure"
        ]




class DebtorsListSerializer(serializers.ModelSerializer):
    interest = InterestSerializer()
    loan_level = LoanLevelSerializer()
    user = UserDetailsSerializer()
   

    class Meta:
        model = UserLoan
        fields = [  "user","interest","loan_level",
                    "paid","amount_requested",
                    "amount_disbursed","loan_date",
                    "loan_due_date","loan_time",
                    "loan_due_time","load_default_status",
                    "number_of_default_days","amount_left","get_loan_default_details","accumulated_amount"
        
        ]


class LoanListSerializer(serializers.ModelSerializer):
    interest = InterestSerializer()
    loan_level = LoanLevelSerializer()
    user = UserDetailsSerializer()
   

    class Meta:
        model = UserLoan
        fields = [  "user","interest","loan_level",
                    "paid","amount_requested",
                    "amount_disbursed","loan_date",
                    "loan_due_date","loan_time",
                    "loan_due_time","load_default_status",
                    "number_of_default_days","amount_left","get_loan_default_details","accumulated_amount"
        
        ]



# class ApplicationListSerializer(serializers.ModelSerializer):
#     interest = InterestSerializer()
#     loan_level = LoanLevelSerializer()
#     user = UserDetailsSerializer()
   

#     class Meta:
#         model = UserLoan
#         fields = [  "user","interest","loan_level",
#                     "paid","amount_requested",
#                     "amount_disbursed","loan_date",
#                     "loan_due_date","loan_time",
#                     "loan_due_time","load_default_status",
#                     "number_of_default_days","amount_left","get_loan_default_details","accumulated_amount"
        
#         ]



class AdminLoginSerializer(serializers.ModelSerializer[CustomUser]):
    phone_number = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):  # type: ignore
        """Get user token."""
        user = CustomUser.objects.get(phone_number=obj.phone_number)
        return {'refresh': user.tokens()['refresh'], 'access': user.tokens()['access'], 'id': str(user.id), "status":True}

    class Meta:
        model = CustomUser
        fields = ['phone_number',  'password', 'tokens']

    def validate(self, data):  # type: ignore
        """Validate and return user login."""
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)
        if phone_number is None:
            raise serializers.ValidationError('A phone number address is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        user = CustomUser.objects.filter(phone_number__exact=phone_number).first()
        if user is None:
            raise serializers.ValidationError('A user with this phone number and password was not found.')

        if user.role != "admin":
            raise serializers.ValidationError('wrong credentials')

        
        valid = user.check_password(password)

        if not valid:
            raise serializers.ValidationError('incorrect credentials')
        return user
        
    def __init__(self, *args, **kwargs):
        super(AdminLoginSerializer, self).__init__(*args, **kwargs)
        self.fields['phone_number'].error_messages['blank'] = 'Please enter your phone number.'
        self.fields['phone_number'].error_messages['invalid'] = 'Please enter a valid phone number.'
        self.fields['password'].error_messages['blank'] = 'Please enter your password.'
    
