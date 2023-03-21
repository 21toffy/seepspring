from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Q
from django.contrib.auth.models import Group
from django.db import transaction
import json
from seepspring.settings import(
    SENDCHAMP_SENDER_ID
)
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from loan.models import Interest, UserLoan
import logging

logger = logging.getLogger(__name__)
from .serializers import (
    AdminLoginSerializer,
    ChangePasswordSerializer,
    GenerateOtpSerializer,
    UserRegistrationSerializer,
    EmploymentDurationCreationSerializer,
    SalaryRangeCreationSerializer,

    UserEmploymentDurationCreationSerializer,
    UserSalaryRangeCreationSerializer,
    LoginSerializer,
    LogoutSerializer,
    LoginUserSerializer,

    EmploymentinformationCreationSerializer,
    EmergencyContactCreationSerializer,
    ColleagueContactCreationSerializer,
    BankAccountDetailsCreationSerializer,
    UserSerializer,

    UserLoanserializer,
LoanInterestSerializer,

)


from .read_serializers import(
    UserRegistrationGetSerializer,
UserEmploymentDurationGetSerializer,
UserSalaryRangeGetSerializer,
EmploymentinformationGetSerializer,
EmergencyContactGetSerializer,
ColleagueContactGetSerializer,
BankAccountDetailsGetSerializer,
)

from rest_framework.permissions import (IsAuthenticated,AllowAny)

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
OtpPhone, validate_mobile_num, BvnData

)
from rest_framework_simplejwt import views as jwt_views


class CustomToken(jwt_views.TokenObtainPairView): 
    serializer_class = AdminLoginSerializer
    token_obtain_pair = jwt_views.TokenObtainPairView.as_view()


from rest_framework import exceptions
from common.utils import (generate_token, generate_four_random_digits, get_international_number, custom_serializer_error)
from django.contrib import auth
import requests

import os
from dotenv import load_dotenv
load_dotenv()
from .messages import *
from common.logic import (SendSMS, GetBVN)




class ResolveBVN(APIView):   
    mock = True     
    def get(self, request, bvn=None):
        if self.mock == True:
            bvn_data = {
                "entity": {
                "bvn": "22350348240",
                "first_name": "ADEOLA",
                "last_name": "AYO",
                "middle_name": "MICHEAL",
                
                "gender": "Male",
                "date_of_birth": "1972-02-19",
                "phone_number1": "08099434292",
                "image": "/9j/3AAQSkZJGgABAgBBBQABAAD/",
                "last_name": "AYO",
                "level_of_account": "Level 2 - Medium Level Accounts",
                "lga_of_origin": "Odo Otin",
                
                "lga_of_residence": "Ilorin South",
                "marital_status": "Single",
                "middle_name": "OLUWATIMILEYIN",
                    
                    "name_on_card": "MICHEAL, ADEOLA A",
                    "nationality": "Nigeria",
                    "nin": "",
                    "phone_number1": "08099434292",
                    "phone_number2": "",
                    "reference": "91b126d1-2467-42fc-b8d5-1cbd32257954",
                    "registration_date": "21-Mar-2018",
                    "residential_address": "24, ADELABU OWODE, ILORIN",
                    "state_of_origin": "Osun State",
                    "state_of_residence": "Kwara State",
                    "title": "Mr",
                    "watch_listed": "NO"
                }
            }
            # with open("./accounts/bvn.json", "r") as f:
            #     bvn = json.load(f)
            return Response({"detail":bvn_data, "status":True}, status.HTTP_200_OK)
        else:
            get_bvn = GetBVN(bvn)
            try:
                bvn_request_data = get_bvn.request_bvn()
            except Exception as e:
                return Response({"detail":str(e), "status":False}, status.HTTP_400_BAD_REQUEST)

            if bvn_request_data.status_code != 200: 
                return Response({"detail":bvn_request_data.json()["error"], "status":False}, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail":bvn_request_data.json(), "status":True}, status.HTTP_200_OK)
            





class UserBankAccountListView(APIView):
    serializer_class = BankAccountDetailsGetSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        active_user_loans = BankAccountDetails.objects.filter(user=request.user)
        serializer = self.serializer_class(active_user_loans, many=True)
        return Response({"detail":serializer.data, "status":True}, status.HTTP_200_OK)
        






class VerifyPhone(APIView):
    def validate_otp(self, otp):
        if len(otp)!= 4:
            raise Exception("Invalid OTP")
        try:
            casted = int(otp)
            return casted
        except Exception as e:
            return e
    def post(self, request):
        otp = request.data.get("otp", None)
        phone = request.data.get("phone", None)
        if otp is None or phone is None:
            return Response({"detail":f"OTP or Phone can not be empty" , "message":f"OTP or Phone can not be empty", "status":False}, status.HTTP_400_BAD_REQUEST)
        try:
            validate_mobile_num(phone)
        except Exception as e:
            return Response({"detail":f"{phone} is not a valid Phone number","message":f"{phone} is not a valid Phone number", "status":False}, status.HTTP_400_BAD_REQUEST)
        try:
            casted = self.validate_otp(otp)
        except Exception as e:
            return Response({"message":f"{otp} is an invalid OTP", "detail":f"{otp} is an invalid OTP","status":False}, status.HTTP_400_BAD_REQUEST)
        check_numbers = OtpPhone.objects.filter(phone=phone, is_deleted=False)
        if check_numbers:
            for check_number in check_numbers:
                saved_code = check_number.code
                if saved_code == casted:
                    check_number.is_deleted=True
                    check_number.save()
                    return Response({"detail":otp_match_success, "status":True}, status.HTTP_200_OK)
                else:
                    return Response({"detail":otp_match_failed, "message":otp_match_failed, "status":False}, status.HTTP_400_BAD_REQUEST)
        return Response({"detail":no_otp,"message":no_otp, "status":False}, status.HTTP_400_BAD_REQUEST)


import logging

# class SendOTPToPhone(APIView):
#     mock =False
#     permission_classes = (AllowAny,)

#     def send_sms_logic(self, data):
#         initialize_sending = SendSMS(data)
#         send_otp = initialize_sending.send_otp()
#         return send_otp

#     def post(self, request):
#         logger = logging.getLogger(__name__)

#         phone = request.data.get("phone", None)
#         try:
#             validate_mobile_num(phone)
#         except Exception as e:
#             logger.error(f"{phone} is not a valid Phone number")
#             return Response({"detail":f"{phone} is not a valid Phone number", "message":f"{phone} is not a valid Phone number", "status":False}, status.HTTP_400_BAD_REQUEST)

#         random_numbers=generate_four_random_digits()
#         built_data = {
#                     "to": get_international_number(phone),
#                     "message": f"Hello your OTP to create an account with us is {random_numbers}",
#                     # "sender_name": openconfig()['sendchamp']['sender_id'],
#                     "sender_name": SENDCHAMP_SENDER_ID,
#                     "route": "non_dnd"
#                     }
#         if phone:
#             check_number = OtpPhone.objects.filter(phone=phone).last()
#             if check_number:
#                 from datetime import datetime, timedelta
#                 time_difference = datetime.now() - check_number.updated_at.replace(tzinfo=None)
#                 if time_difference  < timedelta(seconds=120):
#                     logger.error(wait_two_minutes)
#                     return Response({"detail":wait_two_minutes,"message":wait_two_minutes, "status":False}, status.HTTP_400_BAD_REQUEST)
#                 if time_difference < timedelta(seconds=240) and check_number.count > 3:
#                     logger.error(wait_4_minutes)
#                     return Response({"detail":wait_4_minutes,"message":wait_4_minutes, "status":False}, status.HTTP_400_BAD_REQUEST)

#                 send_otp = self.send_sms_logic(built_data)
#                 check_number.code = random_numbers
#                 check_number.is_deleted = False
#                 check_number.count = check_number.count + 1
#                 check_number.save()
#                 if send_otp["code"] != 200: 
#                     logger.error(send_otp["message"])
#                     return Response({"detail":send_otp["message"],"message":send_otp["message"], "status":False}, status.HTTP_400_BAD_REQUEST)
#                 else:
#                     logger.debug(otp_sent_success)
#                     return Response({"detail":otp_sent_success,"message":otp_sent_success, "status":True}, status.HTTP_200_OK)

#             else:
#                 try:
#                     logger.debug('send champ OTP')
#                     OtpPhone.objects.create(phone=phone, count=1, code = random_numbers)
#                     send_otp = self.send_sms_logic(built_data)
#                     if send_otp["status"] != 200:   
#                         if self.mock == True:
#                             logger.debug(otp_sent_success)
#                             return Response({"detail":otp_sent_success,"message":otp_sent_success, "status":True}, status.HTTP_200_OK)
#                         logger.error(send_otp["message"])
#                         return Response({"detail":send_otp["message"],"message":send_otp["message"], "status":False}, status.HTTP_400_BAD_REQUEST)
#                     else:
#                         logger.debug(otp_sent_success)
#                         return Response({"detail":otp_sent_success,"message":otp_sent_success, "status":True}, status.HTTP_200_OK)
#                 except Exception as e:
#                     logger.error(f"Error occurred while sending OTP to {phone}. Error details: {e}")
#                     return Response({"detail":f"Error occurred while sending OTP to {phone}.", "message":"Error occurred while sending OTP to {phone}.", "status":False}, status.HTTP_400_BAD_REQUEST)



logger = logging.getLogger('send_otp_logger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('otp_logs.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

# use the logger to log messages

class SendOTPToPhone(APIView):
    mock =False
    permission_classes = (AllowAny,)
    def send_sms_logic(self, data):
        
        initialize_sending = SendSMS(data)
        send_otp = initialize_sending.send_otp()
        return send_otp

    def post(self, request):
        
        phone = request.data.get("phone", None)
        try:
            validate_mobile_num(phone)
        except Exception as e:
            logger.error(str(e))
            return Response({"detail":f"{phone} is not a valid Phone number", "message":f"{phone} is not a valid Phone number", "status":False}, status.HTTP_400_BAD_REQUEST)

        random_numbers=generate_four_random_digits()
        built_data = {
                    "to": get_international_number(phone),
                    "message": f"Hello your OTP to create an account with us is {random_numbers}",
                    # "sender_name": openconfig()['sendchamp']['sender_id'],
                    "sender_name": SENDCHAMP_SENDER_ID,
                    "route": "non_dnd"
                    }
        if phone:
            check_number = OtpPhone.objects.filter(phone=phone).last()
            if check_number:
                from datetime import datetime, timedelta
                time_difference = datetime.now() - check_number.updated_at.replace(tzinfo=None)
                if time_difference  < timedelta(seconds=120):
                    return Response({"detail":wait_two_minutes,"message":wait_two_minutes, "status":False}, status.HTTP_400_BAD_REQUEST)
                if time_difference < timedelta(seconds=240) and check_number.count > 3:
                    return Response({"detail":wait_4_minutes,"message":wait_4_minutes, "status":False}, status.HTTP_400_BAD_REQUEST)

                send_otp = self.send_sms_logic(built_data)
                check_number.code = random_numbers
                check_number.is_deleted = False
                check_number.count = check_number.count + 1
                check_number.save()
                if send_otp["code"] != 200: 
                    logger.error(str(send_otp))
                    return Response({"detail":send_otp["message"],"message":send_otp["message"], "status":False}, status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail":otp_sent_success,"message":otp_sent_success, "status":True}, status.HTTP_200_OK)

            else:
                try:
                    logger.debug('send champ OTP')
                    OtpPhone.objects.create(phone=phone, count=1, code = random_numbers)
                    send_otp = self.send_sms_logic(built_data)
                    if send_otp["status"] != 200: 
                        logger.error(str(send_otp))  
                        if self.mock == True:
                            return Response({"detail":otp_sent_success,"message":otp_sent_success, "status":True}, status.HTTP_200_OK)
                        return Response({"detail":send_otp["message"],"message":send_otp["message"], "status":False}, status.HTTP_400_BAD_REQUEST)
                    else:
                        
                        return Response({"detail":otp_sent_success,"message":otp_sent_success, "status":True}, status.HTTP_200_OK)
                except Exception as e:
                    logger.error(str(e))
                    return Response({"detail":str(e), "message":str(e), "status":False}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"phone number field can not be empty","message":"phone number field can not be empty", "status":False}, status.HTTP_400_BAD_REQUEST)
            


 
class VerifyAccountNumber(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            account_number = request.data['account_number']
            bank_code = request.data['bank_code']
            url = f"https://api.paystack.co/bank/resolve?account_number={account_number}&bank_code={bank_code}"
            paystack_api_key = os.getenv('PAYSTACK_API_KEY', None)
            hed = {'Authorization': 'Bearer ' + paystack_api_key}
            r = requests.get(url, headers=hed)
            data = r.json()
            if not data["status"]:
                return  Response({"detail":data["message"],"status":False}, status.HTTP_400_BAD_REQUEST)
            
            name_correlation = self.resolve_name(data.get("data").get("account_name"), request.user.full_name)
            bank_name = data.get("data").get("account_name")
            plartform_name = request.user.full_name
            if name_correlation:
                return Response({"detail":data["message"], "status":True}, status.HTTP_200_OK)
            return Response({"detail":f"Names miss match, Bank name: {bank_name}, Name on our plartform {plartform_name}","status":False}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail":str(e),"status":False}, status.HTTP_400_BAD_REQUEST)
            

    def resolve_name(self, resolved_name, database_name):
        resoled_name_array = resolved_name.lower().split()
        database_name_array = database_name.lower().split()
        probability = 0
        for i in resoled_name_array:
            if i in database_name_array:
                probability +=1
        if probability >=2:
            return True
        else:
            return False


class GenerateOtpView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GenerateOtpSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            phone_number = request.data.get('phone_number', '')
            password = request.data.get('password', '')
            user = auth.authenticate(phone_number=phone_number, password=password)
            if not user:
                raise exceptions.AuthenticationFailed('Invalid credentials, try again')
            if not user.is_active:
                raise exceptions.AuthenticationFailed('Account disabled, contact admin')
            if not user.is_staff:
                raise exceptions.AuthenticationFailed('Auauthorized to view this')
            if not user.groups.filter(name="admin"):
                raise exceptions.AuthenticationFailed('Auauthorized to view this')
            otp_gen = generate_token(phone_number)
            print(otp_gen, 12345)
            results = {
                'otp': otp_gen
            }
            return Response({"auth_status":1,"detail":"Token generated successfully, this is a test message", "details":results, "status":True}, status.HTTP_200_OK)
        return Response({"detail":serializer.errors,  "status":False}, status.HTTP_400_BAD_REQUEST)
    
class EmploymentDurationListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmploymentDurationCreationSerializer

    def get(self, request):
        employment_durations = EmploymentDuration.objects.all()
        serializer = self.serializer_class(employment_durations, many=True)
        return Response({"status": True, "detail":serializer.data}, status.HTTP_200_OK)
    
class SalaryRangeListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SalaryRangeCreationSerializer

    def get(self, request):
        salary_ranges = SalaryRange.objects.all()
        serializer = self.serializer_class(salary_ranges, many=True)
        return Response({"status": True, "detail":serializer.data}, status.HTTP_200_OK)
    






class UserBankAccountCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        us=BankAccountDetailsCreationSerializer(data=request.data,many=False)
        if us.is_valid():
            user = us.save(user = request.user)
            res = {"detail": us.data, "status":  True}
            return Response(res, status=status.HTTP_200_OK)
        else:
            string = (str(us.errors))
            respo = string.split(":")[1].split("=")[1].split(",")[0].split("'")[1] 
            res = {"detail": respo, "status": False}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)



# get the bvn from front
# do the bvn pull
# populate bvn model
# populate user field

class UserRegistration(APIView):
    permission_classes = (AllowAny,)
    # serializer_class = GlobalAccountListSerializer
 
    # @transaction.atomic
    def post(self,request,*args,**kwargs):
        us=UserRegistrationSerializer(data=request.data,many=False)
        if us.is_valid():
            user = us.save()
            try:
                bvn_data = request.data["bvn_data"]
            except Exception as e:
                res = {"detail": str(e), "status":False}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

            try:
                BvnData.objects.create(
                    user = user,
                    bvn = bvn_data.get("bvn", ""),
                    first_name = bvn_data.get("first_name", ""),
                    last_name = bvn_data.get("last_name", ""),
                    middle_name = bvn_data.get("middle_name", ""),
                    gender = bvn_data.get("gender", ""),
                    date_of_birth = bvn_data.get("date_of_birth", ""),
                    phone_number1 = bvn_data.get("phone_number1", ""),
                    level_of_account = bvn_data.get("level_of_account", ""),
                    image = bvn_data.get("image", ""),
                    lga_of_origin = bvn_data.get("lga_of_origin", ""),
                    lga_of_residence = bvn_data.get("lga_of_residence", ""),
                    marital_status = bvn_data.get("marital_status", ""),
                    name_on_card = bvn_data.get("name_on_card", ""),
                    nationality = bvn_data.get("nationality", ""),
                    nin = bvn_data.get("nin", ""),
                    phone_number2 = bvn_data.get("phone_number2", ""),
                    reference = bvn_data.get("reference", ""),
                    registration_date = bvn_data.get("registration_date", ""),
                    residential_address = bvn_data.get("residential_address", ""),
                    state_of_origin = bvn_data.get("state_of_origin", ""),
                    state_of_residence = bvn_data.get("state_of_residence", ""),
                    title = bvn_data.get("title", ""),
                    watch_listed = bvn_data.get("watch_listed", ""),
                )
                res = {"detail": us.data, "status":  True}
                return Response(res, status=status.HTTP_200_OK)
            except Exception as e:
                user.delete()
                res = {"detail": str(e), "status": False}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = us.errors
            string = (str(errors))
            respo = string.split(":")[1].split("=")[1].split(",")[0].split("'")[1] 
            res = {"detail": respo, "status": False}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    def bvn_pull(data):
        mocked=True
        if mocked:
            data["first_name"] = "john"
            data["last_name"] = "doe"
            data["middle_name"] = "middle man"
            data["gender"] = "male"
            data["dob"] = "1988-09-09"
            data["lga_of_origin"] = "lagos-island"
            data["state_of_origin"] = "Lagos"
            data["bvn"] = "bvn"
            data["bvn_phone_number"] = "08023178165"
            data["bvn_address"] = "john"
            return data
        else:
            #logic for live data
            pass






class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': True,
                'detail': 'Password updated successfully',
            }

            return Response(response, status=status.HTTP_200_OK)

        errors = serializer.errors
        string = (str(errors))
        respo = string.split(":")[1].split("=")[1].split(",")[0].split("'")[1] 
        res = {"detail": respo, "status": False}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)




class LoginUserView(APIView):
    def post(self, request, *args, **kwargs):
        
        serializer = LoginUserSerializer(data =request.data)
        if serializer.is_valid():
            phone_number = request.data["phone_number"]
            password = request.data["password"]
            user_profile = CustomUser.objects.filter(phone_number=phone_number).first()
            correct_password = user_profile.check_password(password)            
            if correct_password:
                if user_profile is None:
                    return Response({"message":"You do not have an account", "detail":"You do not have an account", "status":False,}, status=status.HTTP_401_UNAUTHORIZED )
                access_token = AccessToken.for_user(user_profile)
                refresh_token = RefreshToken.for_user(user_profile)
                return Response(
                    {'access_token': str(access_token),
                    'refresh_token': str(refresh_token),
                    "phone_number":user_profile.phone_number,
                    "status": True
                 })
            else:

                return Response({'message': 'No active account found with the given credentials', "data":{}, "status":False}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"message":custom_serializer_error(serializer.errors), "data":{}, "status":False}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                # error_list = [serializer.errors[error][0] for error in serializer.errors]
                errors = serializer.errors
                string = (str(errors))
                respo = string.split(":")[1].split("=")[1].split(",")[0].split("'")[1] 
                res = {"detail": respo, "status": False}          
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            serialized_data = {'refresh':serializer.data['tokens']['refresh'], 'access':serializer.data['tokens']['access']}
            return Response({"detail":serialized_data, "status":True}, status=status.HTTP_200_OK)
        except LookupError as le:
            x = str(le)[1:len(str(le)) -1 ]
            return Response({"detail":[f" {x} can not be empty"], "status":False}, status=status.HTTP_400_BAD_REQUEST)
            
        

      
class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """Validate token and save."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)




class UserMinimalProfileAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        return self.get_user(request, *args, **kwargs)
    def get_user(self, request,*args,**kwargs):
        user = CustomUser.objects.filter(id = self.request.user.id).first()
        user_serializer = UserRegistrationSerializer(user)
        return Response({"detail":user_serializer.data, "status":True}, status=status.HTTP_200_OK)





class UserProfileAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.get_user(request, *args, **kwargs)
    
    def get_user(self, request,*args,**kwargs):
        user = CustomUser.objects.filter(id = self.request.user.id).first()
        _UserEmploymentDuration = UserEmploymentDuration.objects.filter(user = request.user).first()
        _UserSalaryRange = UserSalaryRange.objects.filter(user = request.user).first()
        _Employmentinformation = Employmentinformation.objects.filter(user = request.user).first()
        _EmergencyContact = EmergencyContact.objects.filter(user = request.user).first()
        _ColleagueContact = ColleagueContact.objects.filter(user = request.user).first()
        _BankAccountDetails = BankAccountDetails.objects.filter(user = request.user).first()
        
        user_serializer = UserRegistrationGetSerializer(user)

        _UserEmploymentDurationCreationSerializer = UserEmploymentDurationGetSerializer(_UserEmploymentDuration)
        _UserSalaryRangeCreationSerializer = UserSalaryRangeGetSerializer(_UserSalaryRange)
        _EmploymentinformationCreationSerializer = EmploymentinformationGetSerializer(_Employmentinformation)
        _EmergencyContactCreationSerializer = EmergencyContactGetSerializer(_EmergencyContact)
        _ColleagueContactCreationSerializer = ColleagueContactGetSerializer(_ColleagueContact)
        _BankAccountDetailsCreationSerializer = BankAccountDetailsGetSerializer(_BankAccountDetails)
        z = {"user_details":user_serializer.data, "eployment_duration":_UserEmploymentDurationCreationSerializer.data, "ralary_range":_UserSalaryRangeCreationSerializer.data, "employment_information":_EmploymentinformationCreationSerializer.data,"emergency_contact":_EmergencyContactCreationSerializer.data, "colleague_contact":_ColleagueContactCreationSerializer.data, "bank_details":_BankAccountDetailsCreationSerializer.data}
        return Response({"detail":z, "status":True}, status=status.HTTP_200_OK)










class UserLoanProfileAPIView(APIView):
    # serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        
        available_loan = UserLoan.objects.filter(
                Q(paid=False) |
                Q(active=False) |
                Q(user=request.user)).first()
        if available_loan:

            loan_interest = Interest.objects.filter(id = available_loan.interest.id).first()

        if available_loan:
            user_loan_dictionary = {
                "eligible_to_collect_loan": False,
                 "user":available_loan.user.id,
                 "id":available_loan.id,
                "loan_request_status":available_loan.loan_request_status,
                "amount_requested":available_loan.amount_requested,
                "amount_disbursed":available_loan.amount_disbursed,
                "amount_owed":available_loan.amount_left,
                "loan_date":available_loan.loan_date,
                "loan_due_date":available_loan.loan_due_date,
                "interest":{
                            "id":loan_interest.id,
                            "vat":loan_interest.vat,
                            "service_charge":loan_interest.service_charge,
                            "interest":loan_interest.interest,
                }
            }

            response = {
            'status': True,
            'message': 'user loan profile fetched successfully',
            'detail': user_loan_dictionary,
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
            'status': True,
            'message': 'user loan profile fetched successfully',
            'detail': {"eligible_to_collect_loan": True},
            }
            return Response(response, status=status.HTTP_200_OK)

