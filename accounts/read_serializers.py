from .models import (
CustomUser,
EmploymentDuration,
SalaryRange,
Employmentinformation,
EmergencyContact,
ColleagueContact,
BankAccountDetails,

UserEmploymentDuration,
UserSalaryRange,
)
from rest_framework import serializers

from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.hashers import check_password



class UserRegistrationGetSerializer(serializers.ModelSerializer):


    class Meta:
        model = CustomUser

        fields = [
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "middle_name",
            "dob",
            "gender",
            "nationality",
            # "city",
            "bvn",
            "education",
            "marital_status",
            "current_address",
            "number_of_children",
            "image",
        ]



class UserEmploymentDurationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmploymentDuration
        fields = [
            "id",
            "employment_duration"
        ]


class UserSalaryRangeGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSalaryRange
        fields = [
            "id",
            "salary_range"
        ]



class EmploymentDurationGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentDuration
        fields = [
            "id",
            "level",
            "description",
        ]
class SalaryRangeCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryRange
        fields = [
            "id",
            "level",
            "description",
        ]

class EmploymentinformationGetSerializer(serializers.ModelSerializer):

    employment_duration = EmploymentDurationGetSerializer()
    salary_range = SalaryRangeCreationSerializer()
    class Meta:
        model = Employmentinformation
        fields = [
            "id",
            "employment_status",
            "company_name",
            "company_location",
            "role",
            "employee_id_card",
            "bank_statement",
            "employment_duration",
            "salary_range",
        ]




class EmergencyContactGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = [
            "id",
            "relationship",
            "name",
            "phone_number",
        ]
        

class ColleagueContactGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColleagueContact
        fields = [
            "id",
            "name",
            "phone_number",

        ]


class BankAccountDetailsGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccountDetails
        fields = [
            "id",
            "bank_name",
            "account_number",
            "account_name",
        ]



class UserEmploymentDuratioViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmploymentDuration
        fields = [
            "id",
            "employment_duration"
        ]
        

class UserSalaryRangViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSalaryRange
        fields = [
            "id",
            "salary_range"
        ]

