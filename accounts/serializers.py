from loan.models import Interest, UserLoan
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



class GetuserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser





class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser

        extra_kwargs = {'password': {'write_only': True}}

        fields = [
            "email",
            "password",
            "phone_number",
            "first_name",
            "last_name",
            "middle_name",
            "dob",
            "gender",
            "nationality",
            "current_address",
            "bvn",
            "education",
            "marital_status",
            "number_of_children",
            "image",
            "address_image_url",
            "lga_of_origin",
            "state_of_origin",
            "bvn_phone_number",
            "bvn_address",
            # "city"
        ]
    def create(self, validated_data):
        # create user 
        user = CustomUser.objects.create(
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            first_name = validated_data['first_name']or "",
            last_name = validated_data['last_name']or "",
            middle_name = validated_data['middle_name'],
            dob = validated_data['dob'],
            gender = validated_data['gender']or "",
            nationality = validated_data['nationality']or "",
            # city = validated_data['city'],
            bvn = validated_data['bvn'],
            education = validated_data['education']or "",
            marital_status = validated_data['marital_status']or "",
            current_address = validated_data['current_address']or "",
            number_of_children = validated_data['number_of_children']or "0",
            image = validated_data['image']or "",
            address_image_url = validated_data["address_image_url"] or "",
            lga_of_origin = validated_data["lga_of_origin"] or "",
            state_of_origin = validated_data["state_of_origin"] or "",
            bvn_phone_number = validated_data["bvn_phone_number"] or "",
            bvn_address = validated_data["bvn_address"] or "",
        
        )

        if user.password is not None:
            user.set_password(validated_data['password'])
            user.save()
        
        return user



class UserEmploymentDurationCreationSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(required=False)
    employment_duration_id = serializers.UUIDField(required=False)

    class Meta:
        model = UserEmploymentDuration
        fields = [
            "user_id",
            "employment_duration_id"
        ]
    def create(self, validated_data):
        user_employment_duration = UserEmploymentDuration.objects.create(
            user = validated_data['user'],
            employment_duration = validated_data['employment_duration'],        
        )
        return user_employment_duration

        

class UserSalaryRangeCreationSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(required=False)
    salary_range_id = serializers.UUIDField(required=False)
    class Meta:
        model = UserSalaryRange
        fields = [
            "user_id",
            "salary_range_id"
        ]
    def create(self, validated_data):
        user_salary_range = UserSalaryRange.objects.create(
            user = validated_data['user'],
            salary_range = validated_data['salary_range'],        
        )
        return user_salary_range



class EmploymentDurationCreationSerializer(serializers.ModelSerializer):
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

class EmploymentinformationCreationSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(required=False)
    employment_duration_id = serializers.UUIDField(required=False)
    salary_range_id = serializers.UUIDField(required=False)
    

    class Meta:
        model = Employmentinformation
        fields = [
            "user_id",
            "employment_status",
            "company_name",
            "company_location",
            "role",
            "employee_id_card",
            "bank_statement",
            "employment_duration_id",
            "salary_range_id",
        ]
    def create(self, validated_data):
        employment_creation = Employmentinformation.objects.create(
            user = validated_data['user'],

            employment_status = validated_data['employment_status'],
            company_name = validated_data['company_name'],
            company_location = validated_data['company_location'],
            role = validated_data['role'],
            employee_id_card = validated_data['employee_id_card'],
            bank_statement = validated_data['bank_statement'],            
            employment_duration = validated_data['employment_duration'],
            salary_range = validated_data['salary_range'],        
        )
        return employment_creation




class EmergencyContactCreationSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(required=False)

    class Meta:
        model = EmergencyContact
        fields = [
            "user_id",
            "relationship",
            "name",
            "phone_number",
        ]
        
    def create(self, validated_data):
        employment_creation = EmergencyContact.objects.create(
            
            user = validated_data['user'],
            relationship = validated_data['relationship'],
            name = validated_data['name'],
            phone_number = validated_data['phone_number'],       
        )
        return employment_creation



class ColleagueContactCreationSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(required=False)

    class Meta:
        model = ColleagueContact
        fields = [
            "user_id",
            "name",
            "phone_number",

        ]

    def create(self, validated_data):
        colleague_creation = ColleagueContact.objects.create(
            
            user = validated_data['user'],
            name = validated_data['name'],
            phone_number = validated_data['phone_number'],       
        )
        return colleague_creation



class BankAccountDetailsCreationSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(required=False)

    class Meta:
        model = BankAccountDetails
        fields = [
            "user_id",
            "bank_name",
            "account_number",
            "account_name",
        ]

    def create(self, validated_data):
        bank_account_creation = BankAccountDetails.objects.create(
            user = validated_data['user'],
            bank_name = validated_data['bank_name'],
            account_number = validated_data['account_number'], 
            account_name = validated_data['account_name'],       
        )
        return bank_account_creation





class LoginSerializer(serializers.ModelSerializer[CustomUser]):
    phone_number = serializers.CharField(max_length=255)
    # username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    # is_staff = serializers.BooleanField(read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):  # type: ignore
        """Get user token."""
        user = CustomUser.objects.get(phone_number=obj.phone_number)
        # print(user)
        # print(user.tokens(), 'wow')
        return {'refresh': user.tokens()['refresh'], 'access': user.tokens()['access'], 'id': str(user.id),}

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

        valid = user.check_password(password)

        if not valid:
            raise serializers.ValidationError('incorrect credentials')

        return user

        # if not user.is_active:

class LogoutSerializer(serializers.Serializer[CustomUser]):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type: ignore
        """Validate token."""
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):  # type: ignore
        """Validate save backlisted token."""

        try:
            RefreshToken(self.token).blacklist()

        except TokenError as ex:
            raise Exception.AuthenticationFailed(ex)



def validate_password():

    pass



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





class UserSerializer(serializers.ModelSerializer):
    # employment_duration = UserEmploymentDuratioViewSerializer()
    # salary_range = UserSalaryRangViewSerializer()

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "password",
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
            # "employment_duration",
            # "salary_range",
        )


class UserLoanserializer(serializers.ModelSerializer):
    model = UserLoan
    fields = (
        "user",
        "loan_request_status",
        "amount_requested",
        "amount_disbursed",
        "loan_date",
        "loan_due_date",
        "interest"

    )

class LoanInterestSerializer(serializers.ModelSerializer):
    model = Interest
    fields = (
        "vat",
        "service_charge",
        "interest",
    )


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, )#validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     old_password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = CustomUser
#         fields = ('old_password', 'password', 'password2')


#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError(["Password fields didn't match."])

#         return attrs

#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError([ "Old password is not correct"])
#         return value

#     def update(self, instance, validated_data):

#         instance.set_password(validated_data['password'])
#         instance.save()
#         print(instance)

#         return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
