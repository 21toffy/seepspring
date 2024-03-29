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
CardDetails
)
from rest_framework import serializers
from rest_framework import exceptions
from common.utils import (generate_token, generateKey)
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.hashers import check_password


from .models import CardDetails


class CardDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardDetails
        fields = '__all__'



class CardNumberField(serializers.CharField):
    def to_representation(self, value):
        # Check if the card number is at least 16 digits long
        if len(value) >= 16:
            # Replace the middle 8 digits with asterisks
            return value[:4] + '*' * 8 + value[-4:]
        else:
            return value
class CardDetailsGetSerializer(serializers.ModelSerializer):
    card_no = CardNumberField()

    class Meta:
        model = CardDetails
        fields = [
            "id",
            "card_no",
            "cart_token",
            "card_name",
        ]



class GetuserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser


class LoginUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})



class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser

        extra_kwargs = {'password': {'write_only': True}}

        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "dob",
            "gender",
            "nationality",
            "bvn",
            "education",
            "marital_status",
            "number_of_children",
            "current_address",
            "email",
            "phone_number",
            "lga_of_origin",
            "state_of_origin",
            "city",
            "state_of_residence",
            "password",


        ]
    def create(self, validated_data):
        # create user 
        user = CustomUser.objects.create(
            first_name = validated_data.get("first_name", "First name"),
            middle_name = validated_data.get("middle_name", "middle name"),
            last_name = validated_data.get("last_name", "Last name"),
            dob = validated_data.get("dob", None),
            gender = validated_data.get("gender", "Male"),
            nationality = validated_data.get("nationality", "Nigerian"),
            bvn = validated_data['bvn'],
            education = validated_data['education']or "",
            marital_status = validated_data['marital_status']or "",
            number_of_children = validated_data.get("number_of_children", "0"),
            current_address = validated_data['current_address']or "",
            email = validated_data['email'],
            phone_number = validated_data['phone_number'],
            lga_of_origin = validated_data.get("lga_of_origin", "Lagos Island"),
            state_of_origin = validated_data.get("state_of_origin", "Lagos"),
            city = validated_data['city'],
            state_of_residence = validated_data.get("state_of_residence", "Lagos"),                    
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
    # user_id = serializers.UUIDField(required=False)

    class Meta:
        model = BankAccountDetails
        fields = [
            # "user_id",
            "bank_name",
            "account_number",
            "account_name",
        ]

    # def create(self, validated_data):
    #     bank_account_creation = BankAccountDetails.objects.create(
    #         user = validated_data['user'],
    #         bank_name = validated_data['bank_name'],
    #         account_number = validated_data['account_number'], 
    #         account_name = validated_data['account_name'],       
    #     )
    #     return bank_account_creation





class LoginSerializer(serializers.ModelSerializer[CustomUser]):
    phone_number = serializers.CharField(max_length=255)
    # username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    # is_staff = serializers.BooleanField(read_only=True)

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

        valid = user.check_password(password)

        if not valid:
            raise serializers.ValidationError('incorrect credentials')
        return user
        
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['phone_number'].error_messages['blank'] = 'Please enter your phone number.'
        self.fields['phone_number'].error_messages['invalid'] = 'Please enter a valid phone number.'
        self.fields['password'].error_messages['blank'] = 'Please enter your password.'
        self.fields['password'].error_messages['invalid'] = 'Please enter a valid password.'


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

#         return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)




class GenerateOtpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(max_length=15, min_length=3, write_only=True)
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password']
    # def validate(self, attrs):
    #     password = attrs.get('password', '')

    #     if password < 6 or password > 12:
    #         raise exceptions.AuthenticationFailed('password should not be less than 6 or greated than 12')



from seepspring.settings import(
    OTP_EXPIRY_TIME,
    SECRET_KEY
)
from datetime import datetime
import pyotp
from rest_framework.response import Response
import base64
class AdminLoginSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11, min_length=11)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=68, min_length=8, read_only = True)
    otp = serializers.IntegerField()
    class Meta:
        model = CustomUser
        fields = ['phone_number', 'password', 'tokens', 'otp']
        
    def validate(self, attrs):
        phone_number = attrs.get('phone_number', '')
        password = attrs.get('password', '')
        otp = attrs.get('otp', '')
        tokens = attrs.get('tokens', '')
        user = auth.authenticate(phone_number=phone_number, password=password)
        if not user:
            raise exceptions.AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('Account disabled, contact admin')

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone_number).encode())  # Generating Key
        OTP = pyotp.TOTP(key,interval = OTP_EXPIRY_TIME)  # TOTP Model 
        if OTP.verify(otp):  # Verifying the OTP
            return {
                'phone_number': user.phone_number,
                'full_name': user.full_name,
                'first_name': user.first_name,
                'tokens': user.tokens(),
                "auth_status":2
            }
        raise exceptions.CustomAuthenticationFailed("OTP is wrong/expired")
        





# {
#     "personal_information":{
#         "email" : "gbadamosi@gmail.com",
#         "phone_number" : "08011111122",
#         // "gender" : "Female",
#         "password":"toffy123",
#         // "first_name":"Bilikisu",
#         // "last_name":"Gbadamosi",
#         // "middle_name":"freeman",
#         // "dob":"2019-10-19",
#         // "nationality":"Nigerian",
#         "bvn":"7429429999",
#         "education":"university",
#         "marital_status": "married",
#         "current_address": "23 jesus street",
#         "number_of_children": "3",
#         "image": "https://www.ufebfuebfu.ybf",
#         // "bvn_phone_number":"08011111122",
#         // "bvn_address": "54 uhdud street Lagos",
#         // "lga_of_origin": "lagos island",
#         // "state_of_origin": "lagos",
#         "address_image_url":"http://www.ufebfuebfu.ybf"
#     },
#     "eployment_duration_details":{
#         "employment_duration":"618b402a-d294-4b1c-b386-0ab9f50369cb"
#     },
#     "salary_range_details":{"salary_range":"b0883fce-833d-4871-92f1-90a71d42b772"},

#     "employment_information":{
#                     "employment_status":"Unemployed",
#                     "company_name":"feghas",
#                     "company_location":"omole phase 1",
#                     "role":"intern",
#                     "employee_id_card":"https://www.ufebfuebfu.ybf",
#                     "bank_statement":"https://www.ufebfuebfu.ybf",
#                     "employment_duration":"618b402a-d294-4b1c-b386-0ab9f50369cb",
#                     "salary_range":"9658c8ba-4284-4c87-b64b-b5e54b8cb1cf"
#                     },
#     "emergency_contact": {
#             "relationship":"father",
#             "name":"My daddy",
#             "phone_number":"09088777890"
#     },
#     "colleague_contact": {
#             "name":"ayomide",
#             "phone_number":"08097283838"
#     },
#     "bank_details": {
#             "bank_name":"GT bank",
#             "account_number": "098392999",
#             "account_name":"tofunmi okedeji"
#     }
                
# }