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



