from accounts.read_serializers import UserDetailsSerializer, UserRegistrationGetSerializer
from common import constants
from accounts.models import (CustomUser)
from rest_framework import serializers

from loan.models import LoanLevel, UserLoan
from loan.serializers import InterestSerializer






class DashboardUserListSerializer(serializers.ModelSerializer):
    # contact = ImageSerializer(source='image_set', many=True)

    class Meta:
        model = CustomUser
        fields = [  "user_level","full_name",
                    "email","phone_number",
                    "dob","gender",
                    "state_of_origin","marital_status",
                    "current_address","bvn_phone_number",
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
    
