from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Q

from django.db import transaction

from loan.models import Interest, UserLoan


from .serializers import (
    ChangePasswordSerializer,
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
)


from rest_framework.settings import api_settings


class EmploymentDurationListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmploymentDurationCreationSerializer

    def get(self, request):
        employment_durations = EmploymentDuration.objects.all()
        serializer = self.serializer_class(employment_durations, many=True)
        return Response({"message":"success", "data":serializer.data, "status":status.HTTP_200_OK}, status.HTTP_200_OK)
    
class SalaryRangeListView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SalaryRangeCreationSerializer

    def get(self, request):
        salary_ranges = SalaryRange.objects.all()
        serializer = self.serializer_class(salary_ranges, many=True)
        return Response({"message":"success", "data":serializer.data, "status":status.HTTP_200_OK}, status.HTTP_200_OK)
    






class UserRegistration(APIView):
    permission_classes = (AllowAny,)
    # serializer_class = GlobalAccountListSerializer

    @transaction.atomic
    def post(self, request, format=None):
        user_serializer = UserRegistrationSerializer(data=request.data['personal_information'])
        employment_serializer = EmploymentinformationCreationSerializer(data=request.data['employment_information'])        
        emergency_contact_serializer = EmergencyContactCreationSerializer(data=request.data['emergency_contact'])
        colleague_contact_serializer = ColleagueContactCreationSerializer(data=request.data['colleague_contact'])        
        bank_details_serializer = BankAccountDetailsCreationSerializer(data=request.data['bank_details'])
        try:
            
            if user_serializer.is_valid():
                with transaction.atomic():
                    personal_information_object = user_serializer.save()
                if employment_serializer.is_valid():
                    employment_duration_object = EmploymentDuration.objects.filter(id = request.data['eployment_duration_details']["employment_duration"]).first()
                    salary_range_object = SalaryRange.objects.filter(id = request.data['salary_range_details']["salary_range"]).first()
                    
                    employment_serializer.save(user = personal_information_object, employment_duration  = employment_duration_object , salary_range=salary_range_object )
                    if emergency_contact_serializer.is_valid():
                        emergency_contact_serializer.save(user = personal_information_object)   
                        if colleague_contact_serializer.is_valid():
                            colleague_contact_serializer.save(user = personal_information_object)
                            if bank_details_serializer.is_valid():
                                bank_details_serializer.save(user = personal_information_object)
                                return Response({"message":"success", "data":user_serializer.data , "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
                            else:
                                personal_information_object.delete()
                                return Response(bank_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            personal_information_object.delete()
                            return Response(colleague_contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        personal_information_object.delete()
                        return Response(emergency_contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    personal_information_object.delete()
                    return Response(employment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    personal_information_object.delete()
                except:
                    pass
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LookupError as ke:
            try:
                personal_information_object.delete()
            except UnboundLocalError:
                x = str(ke)[1:len(str(ke)) -1 ]
                return Response({x:[f" {x} can not be empty"]}, status=status.HTTP_400_BAD_REQUEST)
            
            x = str(ke)[1:len(str(ke)) -1 ]
            return Response({x:[f" {x} field can not be empty"]}, status=status.HTTP_400_BAD_REQUEST)







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
        return Response(data={"message":"user profile", "user":z}, status=status.HTTP_200_OK)



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


