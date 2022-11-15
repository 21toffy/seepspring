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

from loan.models import Interest, UserLoan

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
from common.utils import (generate_token, generate_four_random_digits, openconfig)
from django.contrib import auth
import requests

import os
from dotenv import load_dotenv
load_dotenv()
from .messages import *
from common.logic import (SendSMS, GetBVN)




class ResolveBVN(APIView):   
    mock = False     
    def get(self, request, bvn=None):
        if self.mock == True:
            with open("./accounts/bvn.json", "r") as f:
                bvn = json.load(f)
            return Response({"detail":bvn["entity"], "status":"success"}, status.HTTP_200_OK)
        else:
            get_bvn = GetBVN(bvn)
            try:
                bvn_request_data = get_bvn.request_bvn()
            except Exception as e:
                return Response({"detail":str(e), "status":"failed"}, status.HTTP_400_BAD_REQUEST)

            if bvn_request_data.status_code != 200: 
                return Response({"detail":bvn_request_data.json()["error"], "status":"failed"}, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail":bvn_request_data.json(), "status":"success"}, status.HTTP_200_OK)
            

# class ResolveBVN(APIView):        
#     def get(self, request, bvn=None):
#         get_bvn = GetBVN(bvn)
#         try:
#             bvn_request_data = get_bvn.request_bvn()
#         except Exception as e:
#             return Response({"detail":str(e)}, status.HTTP_400_BAD_REQUEST)

#         if bvn_request_data.status_code == 401: 
#             return Response({"detail":"something went wrong, if issue persist please contact us, thanks"}, status.HTTP_400_BAD_REQUEST)
#         if bvn_request_data.status_code == 400: 
#             return Response({"detail":"something went wrong, if issue persist please contact us, thanks"}, status.HTTP_400_BAD_REQUEST)        
#         else:
#             return Response({"detail":bvn_request_data.text}, status.HTTP_200_OK)
        






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
            return Response({"detail":f"OTP or Phone can not be empty", "status":"failed"}, status.HTTP_400_BAD_REQUEST)
        try:
            validate_mobile_num(phone)
        except Exception as e:
            return Response({"detail":f"{phone} is not a valid Phone number", "status":"failed"}, status.HTTP_400_BAD_REQUEST)
        try:
            casted = self.validate_otp(otp)
        except Exception as e:
            return Response({"detail":f"{otp} is an invalid OTP", "status":"failed"}, status.HTTP_400_BAD_REQUEST)
        check_numbers = OtpPhone.objects.filter(phone=phone, is_deleted=False)
        if check_numbers:
            for check_number in check_numbers:
                saved_code = check_number.code
                if saved_code == casted:
                    check_number.is_deleted=True
                    check_number.save()
                    return Response({"detail":otp_match_success, "status":"success"}, status.HTTP_200_OK)
                else:
                    return Response({"detail":otp_match_failed, "status":"failed"}, status.HTTP_400_BAD_REQUEST)
        return Response({"detail":no_otp, "status":"failed"}, status.HTTP_400_BAD_REQUEST)

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
            return Response({"detail":f"{phone} is not a valid Phone number", "status":"failed"}, status.HTTP_400_BAD_REQUEST)

        random_numbers=generate_four_random_digits()
        built_data = {
                    "to": phone,
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
                    return Response({"detail":wait_two_minutes, "status":"failed"}, status.HTTP_400_BAD_REQUEST)
                if time_difference > timedelta(seconds=240) and check_number.count < 3:
                    return Response({"detail":wait_4_minutes, "status":"failed"}, status.HTTP_400_BAD_REQUEST)

                send_otp = self.send_sms_logic(built_data)
                check_number.code = random_numbers
                check_number.is_deleted = False
                check_number.count = check_number.count + 1
                check_number.save()
                if send_otp["code"] != 200:   
                    return Response({"detail":send_otp["message"], "status":"failed"}, status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail":otp_sent_success, "status":"success"}, status.HTTP_200_OK)

            else:
                try:
                    OtpPhone.objects.create(phone=phone, count=1, code = random_numbers)
                    send_otp = self.send_sms_logic(built_data)
                    if send_otp["status"] != 200:   
                        if self.mock == True:
                            return Response({"detail":otp_sent_success, "status":"success"}, status.HTTP_200_OK)
                        return Response({"detail":send_otp["message"], "status":"failed"}, status.HTTP_400_BAD_REQUEST)
                    else:
                        
                        return Response({"detail":otp_sent_success, "status":"success"}, status.HTTP_200_OK)
                except Exception as e:
                    return Response({"detail":str(e), "status":"failed"}, status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"phone number field can not be empty", "status":"failed"}, status.HTTP_400_BAD_REQUEST)
            


 
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
                return  Response({"detail":data["message"],"data":{"status":False},"status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
            
            name_correlation = self.resolve_name(data.get("data").get("account_name"), request.user.full_name)
            bank_name = data.get("data").get("account_name")
            plartform_name = request.user.full_name
            if name_correlation:
                return Response({"detail":data["message"], "data":{"status":True, "name":bank_name.lower()}, "status":status.HTTP_200_OK}, status.HTTP_200_OK)
            return Response({"detail":f"Names miss match, Bank name: {bank_name}, Name on our plartform {plartform_name}","data":{"status":False},"status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail":str(e),"data":{"status":False},"status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
            

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
            results = {
                'otp': generate_token(phone_number)
            }
            return Response({"auth_status":1,"detail":"Token generated successfully, this is a test message", "data":results, "status":status.HTTP_200_OK}, status.HTTP_200_OK)
        return Response({"detail":serializer.errors,  "status":status.HTTP_400_BAD_REQUEST}, status.HTTP_400_BAD_REQUEST)
        
    


class EmploymentDurationListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmploymentDurationCreationSerializer

    def get(self, request):
        employment_durations = EmploymentDuration.objects.all()
        serializer = self.serializer_class(employment_durations, many=True)
        return Response({"detail":"success", "data":serializer.data, "status":status.HTTP_200_OK}, status.HTTP_200_OK)
    
class SalaryRangeListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SalaryRangeCreationSerializer

    def get(self, request):
        salary_ranges = SalaryRange.objects.all()
        serializer = self.serializer_class(salary_ranges, many=True)
        return Response({"detail":"success", "data":serializer.data, "status":status.HTTP_200_OK}, status.HTTP_200_OK)
    






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
                res = {"detail": str(e), "status": "failed"}
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
                res = {"detail": us.data, "status": "success"}
                return Response(res, status=status.HTTP_200_OK)
            except Exception as e:
                user.delete()
                res = {"detail": str(e), "status": "failed"}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = us.errors
            string = (str(errors))
            respo = string.split(":")[1].split("=")[1].split(",")[0].split("'")[1] 
            res = {"detail": respo, "status": "failed"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

    # def get(self,request,pk):
    #     book_obj=Book.objects.filter(pk=pk).first()
    #     bs=BookSerializers(book_obj)
    #     return Response(bs.data)
 
    # def put(self,request,pk):
    #     book_obj=Book.objects.filter(pk=pk).first()
    #              bs=BookSerializers(book_obj,data=request.data)
    #     if bs.is_valid():
    #         bs.save()
    #         return Response(bs.data)
    #     else:
    #         return HttpResponse(bs.errors)

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


    # def post(self, request, format=None):
    #     user_serializer = UserRegistrationSerializer(data=request.data['personal_information'])
    #     # user_serializer = UserRegistrationSerializer(data=self.bvn_pull(request.data["personal_information"]))        
    #     employment_serializer = EmploymentinformationCreationSerializer(data=request.data['employment_information'])        
    #     emergency_contact_serializer = EmergencyContactCreationSerializer(data=request.data['emergency_contact'])
    #     colleague_contact_serializer = ColleagueContactCreationSerializer(data=request.data['colleague_contact'])        
    #     bank_details_serializer = BankAccountDetailsCreationSerializer(data=request.data['bank_details'])
    #     try:
    #         if user_serializer.is_valid():
    #             with transaction.atomic():
    #                 personal_information_object = user_serializer.save()
    #                 group, created = Group.objects.get_or_create(name="client")
    #                 personal_information_object.groups.add(group)
    #             if employment_serializer.is_valid():
    #                 employment_duration_object = EmploymentDuration.objects.filter(id = request.data['eployment_duration_details']["employment_duration"]).first()
    #                 salary_range_object = SalaryRange.objects.filter(id = request.data['salary_range_details']["salary_range"]).first()
                    
    #                 employment_serializer.save(user = personal_information_object, employment_duration  = employment_duration_object , salary_range=salary_range_object )
    #                 if emergency_contact_serializer.is_valid():
    #                     emergency_contact_serializer.save(user = personal_information_object)   
    #                     if colleague_contact_serializer.is_valid():
    #                         colleague_contact_serializer.save(user = personal_information_object)
    #                         if bank_details_serializer.is_valid():
    #                             bank_details_serializer.save(user = personal_information_object)
    #                             return Response({"detail":"success", "data":user_serializer.data , "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    #                         else:
    #                             personal_information_object.delete()
    #                             return Response(bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #                     else:
    #                         personal_information_object.delete()
    #                         return Response(colleague_contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #                 else:
    #                     personal_information_object.delete()
    #                     return Response(emergency_contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #             else:
    #                 personal_information_object.delete()
    #                 return Response(employment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             try:
    #                 personal_information_object.delete()
    #             except:
    #                 pass
    #             return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     except LookupError as ke:
    #         try:
    #             personal_information_object.delete()
    #         except UnboundLocalError:
    #             x = str(ke)[1:len(str(ke)) -1 ]
    #             return Response({x:[f" {x} can not be empty"]}, status=status.HTTP_400_BAD_REQUEST)
            
    #         x = str(ke)[1:len(str(ke)) -1 ]
    #         return Response({x:[f" {x} field can not be empty"]}, status=status.HTTP_400_BAD_REQUEST)







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
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer
    def post(self, request):
        try:
            """Return user after login."""
            # user = request.data.get('user', {})
            data = self.check_ifempty(request.data)
            if data != 1:
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                error_list = [serializer.errors[error][0] for error in serializer.errors]             
                return Response({'message':error_list[0]}, status=status.HTTP_400_BAD_REQUEST)
            serialized_data = {'phone_number': serializer.data['phone_number'], 'refresh':serializer.data['tokens']['refresh'], 'access':serializer.data['tokens']['access'], 'id': serializer.data["tokens"]['id']}
            return Response(serialized_data, status=status.HTTP_200_OK)
        except LookupError as le:
            x = str(le)[1:len(str(le)) -1 ]
            return Response({x:[f" {x} can not be empty"]}, status=status.HTTP_400_BAD_REQUEST)
            

    def check_ifempty(self, data):
        password = data['password']
        phone_number = data['phone_number']
        if phone_number == '':
            return {'phone_number': ['phone number can not be empty']}
        if password == '':
            return {'password': ['Password can not be empty']}
        if phone_number and password:
            return 1
        

      
class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        """Validate token and save."""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)



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
        return Response(data={"detail":"user profile", "user":z}, status=status.HTTP_200_OK)



class UserLoanProfileAPIView(APIView):
    # serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            available_loan = UserLoan.objects.filter(
                Q(paid=False) |
                Q(active=False) |
                Q(user=request.user)).first()
            loan_interest = Interest.objects.filter(id = available_loan.interest.id).first()
        except AttributeError:
            response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'use loan profile fetched successfully',
            'data': {"loan_status":{"eligible_to_collect_loan": False}},
            }
            return Response(response, status=status.HTTP_200_OK)

        if available_loan:
            user_loan_dictionary = {
                "loan_status":{"eligible_to_collect_loan": False},
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
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'user loan profile fetched successfully',
            'data': user_loan_dictionary,
            }

            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'use loan profile fetched successfully',
            'data': {"loan_status":available_loan.get_loan_default_details},
            }
            return Response(response, status=status.HTTP_200_OK)


