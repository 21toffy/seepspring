from datetime import datetime
from django.shortcuts import render
from accounts.models import CustomUser
from loan.models import UserLoan, LoanRepayment, AmountDisbursed
from . import serializers
from common import constants
from common.utils import get_date_yyyy_mm_dd, get_first_serializer_error
from django.db.models import Q
from common.messages import (
    eployee_creation_email_subject
) 
from django.conf import settings

from rest_framework import generics
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,AllowAny)
from decimal import *
from django.db.models import Sum
from django.db.models import Q
from rest_framework import pagination
from django.db import transaction

from common.email_utils import send_email, SendChampEmailSender

 
class EmployeeCreation(APIView):
    permission_classes = (AllowAny,)
    email = "sendchamp"
    # email = "custom"

    # serializer_class = GlobalAccountListSerializer

    @transaction.atomic
    def post(self,request,*args,**kwargs):
        us=serializers.EmployeeCreationSerializer(data=request.data["user_details"],many=False)

        if us.is_valid():
            user = us.save()
            es = serializers.EmployeeSerializer(data=request.data["employee_details"], context={'request': request, 'user': user})
            if es.is_valid():
                x = es.save()
                if self.email == "sendchamp":
                    sender = SendChampEmailSender()
                    response = sender.send_email(
                        subject=eployee_creation_email_subject,
                        to_email=us.validated_data["email"],
                        to_name=us.validated_data["first_name"],
                        from_email=settings.ADMIN_EMAIL,
                        from_name="Admin",
                        message_body_type= "text",
                        message_body_value = f"Hello, '{user.first_name}' welcome to Kulucash, your password is '{x.default_passsword}'. Please login to change"
                    )

                    if response["code"] != 200:
                        user.delete()
                        x.delete()
                        return Response({"detail":response["message"],"message":response["message"], "status":False}, status.HTTP_400_BAD_REQUEST)
                    else:
                        return Response({"detail":"account created successfully","message":"account created successfully", "status":True}, status.HTTP_200_OK)

                else:
                    send_email(
                        subject=eployee_creation_email_subject,
                        to_email=us.validated_data["email"],
                        context={'user': user},
                        template_name='email/employee_creation_notification.html'
                    )
                    print(send_email, "00000000000000000000000000000000000000000000000000")

            return Response({"detail":get_first_serializer_error(es.errors), "status":False}, status=status.HTTP_400_BAD_REQUEST)
        else:
            errors = us.errors
            string = (str(errors))
            respo = string.split(":")[1].split("=")[1].split(",")[0].split("'")[1] 
            res = {"detail": respo, "status": False}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)








# view to list out all debtors 
class DebtorsApiView(APIView):
    permission_classes = (IsAuthenticated,)
    mocked = False
    def get(self, request, *args, **kwargs):
        query_param = request.GET.get('query')
        if query_param is not None:
            all_debtors = UserLoan.objects.filter(active = True,
            paid = False,
            loan_request_status =constants.DISBURSED).filter(Q(user__first_name__icontains=query_param) | Q(user__last_name__icontains=query_param))
        else:
            all_debtors = UserLoan.objects.filter(active = True, paid = False, loan_request_status =constants.DISBURSED)
        serializer = serializers.DebtorsListSerializer(all_debtors, many=True)
        return Response({"status":True, "detail":serializer.data}, status.HTTP_200_OK)




class UserLoanDetailView(generics.RetrieveAPIView):
    queryset = UserLoan.objects.all()
    serializer_class = serializers.UserLoanSerializer
    permission_classes = [AllowAny]
    

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        user_loan = self.get_object(pk=pk)
        serializer = serializers.UserLoanSerializer(user_loan)
        loan_repayments = LoanRepayment.objects.filter(user_loan=user_loan)
        serializer_repayment = serializers.LoanRepaymentSerializer(loan_repayments, many=True)
        return Response({'user_loan': serializer.data, 'loan_repayments': serializer_repayment.data})
   
    def get_object(self, pk=None):
        queryset = self.filter_queryset(self.get_queryset())
        if pk is not None:
            return queryset.filter(pk=pk).first()
        return super().get_object()





class PendingListAPIViewListAPIView(APIView):

    def post(self, request):
        # entity = request.data.get('entity')
        page = request.data.get('page', 1)
        per_page = request.data.get('perPage', 100)        
        filters = request.data.get('filters', None)

        default_filter = [
                {
                "field": "bank_name",
                "value":""
                },
                                {
                "field": "account_number",
                "value":""
                },
                {
                "field": "user_id",
                "value":""
                },
                {
                    "field": "amount_requested",
                    "value": 0
                }
            ]

        if filters is not None and len(filters)< 1:
            filters = default_filter
        if filters is None:
            filters = default_filter
        
        # Apply filters to queryset
        queryset = UserLoan.objects.filter(loan_request_status="PENDING")

        try:
            for filter in filters:
                field = filter['field']
                value = filter['value']
                if field == "amount_requested":
                    if int(value) > 0:
                        queryset = queryset.filter(**{field: value})
                if field == 'user_id':
                    if value != "":
                        queryset = queryset.filter(**{"user_loan__user__id": value})

                if field == 'account_number':
                    if value != "":
                        queryset = queryset.filter(**{"user_loan__account_number__account_number": value})
                
                if field == 'bank_name':
                    if value != "":
                        queryset = queryset.filter(**{"user_loan__account_number__bank_name": value})

            # print(queryset, value, field)
        except Exception as e:
            return Response(({
                "message": str(e),
                "payload": {
                    "gridData": [],
                    "totalCount": 0
                },
                "status": "BAD_REQUEST",
                "statusCode": 400
            }), status=status.HTTP_400_BAD_REQUEST)
        paginator = pagination.PageNumberPagination()
        paginator.page_size = per_page
        result_page = paginator.paginate_queryset(queryset, request)
        total_count = paginator.page.paginator.count

  
        serializer = serializers.LoanApplicationListSerializer(result_page, many=True)
        grid_data = serializer.data

        # Return response
        return Response({
            "message": "SUCCESS",
            "payload": {
                "gridData": grid_data,
                "totalCount": total_count
            },
            "status": "OK",
            "statusCode": 200
        })


class AmountDisbursedListAPIView(APIView):

    def post(self, request):
        # entity = request.data.get('entity')
        page = request.data.get('page', 1)
        per_page = request.data.get('perPage', 100)
        filters = request.data.get('filters', None)

        default_filter = [
                {
                "field": "amount_disbursed",
                "value":0
                },
                {
                "field": "bank_name",
                "value":""
                },
                                {
                "field": "account_number",
                "value":""
                },
                {
                "field": "user_id",
                "value":""
                },
                {
                    "field": "disbursement_date",
                    "value": get_date_yyyy_mm_dd()
                },
                {
                    "field": "bank_name",
                    "value": ""
                },
                                {
                    "field": "transaction_reference",
                    "value": ""
                }
            ]

        if filters is not None and len(filters)< 1:
            filters = default_filter
        if filters is None:
            filters = default_filter
        
        queryset = AmountDisbursed.objects.all().order_by('-disbursement_date')
        # print(queryset, 11223599)
        for filter in filters:
            field = filter['field']
            value = filter['value']
            if field == "disbursement_date":
                if value != "":
                    queryset = queryset.filter(**{"disbursement_date__year":value[0:4], "disbursement_date__month":value[5:7], "disbursement_date__day":value[8:]})            
            
            if field == 'amount_disbursed':
                if int(value) > 0:
                    queryset = queryset.filter(**{field: value})

            if field == 'transaction_refernce':
                if value != "":
                    queryset = queryset.filter(**{field: value})

            if field == 'user_id':
                if value != "":
                    queryset = queryset.filter(**{"user_loan__user__id": value})

            if field == 'transaction_refernce':
                if value != "":
                    queryset = queryset.filter(**{field: value})

            if field == 'account_number':
                if value != "":
                    queryset = queryset.filter(**{"user_loan__account_number__account_number": value})
            
            if field == 'bank_name':
                if value != "":
                    queryset = queryset.filter(**{"user_loan__account_number__bank_name": value})
            
        

        # Paginate queryset
        paginator = pagination.PageNumberPagination()
        paginator.page_size = per_page
        result_page = paginator.paginate_queryset(queryset, request)
        total_count = paginator.page.paginator.count

        # Serialize queryset
        serializer = serializers.AmountDisbursedListSerializer(result_page, many=True)
        grid_data = serializer.data

        # Return response
        return Response({
            "message": "SUCCESS",
            "payload": {
                "gridData": grid_data,
                "totalCount": total_count
            },
            "status": "OK",
            "statusCode": 200
        })



class LoanRepaymentListAPIView(APIView):

    def post(self, request):
        # entity = request.data.get('entity')
        page = request.data.get('page', 1)
        per_page = request.data.get('perPage', 100)
        filters = request.data.get('filters', None)

        default_filter = [
                {
                "field": "amount",
                "value":0
                },
                {
                    "field": "repayment_date",
                    "value": get_date_yyyy_mm_dd()
                },
                {
                    "field": "transaction_refernce",
                    "value": ""
                }
            ]

        if filters is not None and len(filters)< 1:
            filters = default_filter
        if filters is None:
            filters = default_filter
        
        queryset = LoanRepayment.objects.all().order_by('-repayment_date')
        for filter in filters:
            field = filter['field']
            value = filter['value']
            if field == "repayment_date":
                if value != "":
                    queryset = queryset.filter(**{"repayment_date__year":value[0:4], "repayment_date__month":value[5:7], "repayment_date__day":value[8:]})            
            if field == 'amount':
                if int(value) > 0:
                    queryset = queryset.filter(**{field: value})
            if field == 'transaction_refernce':
                if value != "":
                    queryset = queryset.filter(**{field: value})
        

        # Paginate queryset
        paginator = pagination.PageNumberPagination()
        paginator.page_size = per_page
        result_page = paginator.paginate_queryset(queryset, request)
        total_count = paginator.page.paginator.count

        # Serialize queryset
        serializer = serializers.LoanRepaymentListSerializer(result_page, many=True)
        grid_data = serializer.data

        # Return response
        return Response({
            "message": "SUCCESS",
            "payload": {
                "gridData": grid_data,
                "totalCount": total_count
            },
            "status": "OK",
            "statusCode": 200
        })






class LoanApplicationListAPIView(APIView):

    def post(self, request):
        # entity = request.data.get('entity')
        page = request.data.get('page', 1)
        per_page = request.data.get('perPage', 100)        
        filters = request.data.get('filters', None)

        default_filter = [
                {
                "field": "loan_date",
                "value": get_date_yyyy_mm_dd()
                },
                {
                    "field": "loan_request_status",
                    "value": "PENDING"
                },
                {
                    "field": "amount_requested",
                    "value": 10000000
                }
            ]

        if filters is not None and len(filters)< 1:
            filters = default_filter
        if filters is None:
            filters = default_filter
        


        # Apply filters to queryset
        queryset = UserLoan.objects.all()

        try:
            for filter in filters:
                field = filter['field']
                value = filter['value']
                if field == "amount_requested" and value == int(10000000):
                    queryset = queryset.filter(**{"amount_requested__lte": 3000000.00})
                    print("i am hereeee")
                else:
                    queryset = queryset.filter(**{field: value})

            # print(queryset, value, field)
        except Exception as e:
            return Response(({
                "message": str(e),
                "payload": {
                    "gridData": [],
                    "totalCount": 0
                },
                "status": "BAD_REQUEST",
                "statusCode": 400
            }), status=status.HTTP_400_BAD_REQUEST)
        paginator = pagination.PageNumberPagination()
        paginator.page_size = per_page
        result_page = paginator.paginate_queryset(queryset, request)
        total_count = paginator.page.paginator.count

  
        serializer = serializers.LoanApplicationListSerializer(result_page, many=True)
        grid_data = serializer.data

        # Return response
        return Response({
            "message": "SUCCESS",
            "payload": {
                "gridData": grid_data,
                "totalCount": total_count
            },
            "status": "OK",
            "statusCode": 200
        })

class ClientListAPIView(APIView):

    def post(self, request):
        # entity = request.data.get('entity')
        page = request.data.get('page', 1)
        per_page = request.data.get('perPage', 100)
        filters = request.data.get('filters', None)

        default_filter = [
                {
                "field": "first_name",
                "value":""
                },
                {
                    "field": "last_name",
                    "value": ""
                },
                {
                    "field": "email",
                    "value": ""
                }
            ]

        if filters is not None and len(filters)< 1:
            filters = default_filter
        if filters is None:
            filters = default_filter
        

        # Apply filters to queryset
        queryset = CustomUser.objects.all()
        for filter in filters:
            field = filter['field']
            value = filter['value']
            if value != "":
                queryset = queryset.filter(**{field: value})

        # Paginate queryset
        paginator = pagination.PageNumberPagination()
        paginator.page_size = per_page
        result_page = paginator.paginate_queryset(queryset, request)
        total_count = paginator.page.paginator.count

        # Serialize queryset
        serializer = serializers.userListSerializer(result_page, many=True)
        grid_data = serializer.data

        # Return response
        return Response({
            "message": "SUCCESS",
            "payload": {
                "gridData": grid_data,
                "totalCount": total_count
            },
            "status": "OK",
            "statusCode": 200
        })


class AdminLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.AdminLoginSerializer
    def post(self, request):

        return Response({"status":True, "detail":serializers.data}, status.HTTP_200_OK)




class AdminLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.AdminLoginSerializer
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                # error_list = [serializer.errors[error][0] for error in serializer.errors]
                errors = serializer.errors
                string = (str(errors))
                # print(list(errors.keys()[0]),9999999)
                respo = string.split(":")[1].split("=")[1].split(",")[0].split("'")[1] 
                joined_data = respo if list(errors.keys())[0]== 'non_field_errors' else list(errors.keys())[0] + " " + respo
                res = {"detail": joined_data, "status": False}          
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
            serialized_data = {'refresh':serializer.data['tokens']['refresh'], 'access':serializer.data['tokens']['access']}
            return Response({"detail":serialized_data, "status":True}, status=status.HTTP_200_OK)
        except LookupError as le:
            x = str(le)[1:len(str(le)) -1 ]
            return Response({"detail":[f" {x} can not be empty"], "status":False}, status=status.HTTP_400_BAD_REQUEST)
        



class AdminDashboard(APIView):

    permission_classes = (IsAuthenticated,)
    mocked = False
    def get(self, request,filter,query=None ,*args, **kwargs):
        from datetime import datetime, timedelta
        query_param = request.GET.get('query')
        if query_param is not None :
            all_clients = CustomUser.objects.filter(groups__name='client').filter(Q(first_name__icontains=query_param) | Q(last_name__icontains=query_param))
        else:
            all_clients = CustomUser.objects.filter(is_staff=False , groups__name='client')
        client_data = []
        for client in all_clients:
            client_dict = {
                "user_level":client.user_level,
                "full_name":client.full_name,
                "email":client.email,
                "phone_number":client.phone_number,
                "dob":client.dob,
                "gender":client.gender,
                "state_of_origin":client.state_of_origin,
                "marital_status":client.marital_status,
                "current_address":client.current_address,
                "bvn_phone_number":client.bvn_phone_number,
                "user_level":client.user_level,
                "emergency_contact_relationship":None if client.emergencycontact_set.first() is None else client.emergencycontact_set.first().relationship,
                "emergency_contact_name": None if client.emergencycontact_set.first() is None else client.emergencycontact_set.first().name,
                "emergency_contact_phone_number":None if client.emergencycontact_set.first() is None else client.emergencycontact_set.first().phone_number,
                "colleague_contact_name":None if client.colleaguecontact_set.first() is None else client.colleaguecontact_set.first().name,
                "colleague_contact_phone_number":None if client.colleaguecontact_set.first() is None else client.colleaguecontact_set.first().phone_number,
            }
            client_data.append(client_dict)
        loan_statuses = [constants.DISBURSED, constants.LATE, constants.PART_SETTLEMENT]
        if filter == '1':
            days = 1
        elif filter == "7":
            days = 7
        elif filter == "30":
            days = 30
        else:
            days = 'all'

        if days != 'all':
            print('not all')
            amount_requested = UserLoan.objects.filter(
            active = True, 
            paid = False,
            loan_request_status__in =loan_statuses,
            created_at__lte=datetime.now()- timedelta(days=days)
            ).aggregate(amount_requested=Sum('amount_requested'))

            amount_disbursed =  UserLoan.objects.filter(
            active = True, 
            paid = False,
            loan_request_status__in =loan_statuses,
            created_at__lte=datetime.now()- timedelta(days=days)
            ).aggregate(amount_disbursed=Sum('amount_disbursed'))

            amount_owed = UserLoan.objects.filter(
            active = True,
            paid = False,
            loan_request_status__in =loan_statuses,
            created_at__lte=datetime.now()- timedelta(days=days)
            ).aggregate(amount_left=Sum('amount_left'))
        else:
            print('all')
            amount_requested = UserLoan.objects.filter(
            active = True, 
            paid = False,
            loan_request_status__in =loan_statuses
            ).aggregate(amount_requested=Sum('amount_requested'))

            amount_disbursed =  UserLoan.objects.filter(
            active = True, 
            paid = False,
            loan_request_status__in =loan_statuses
            ).aggregate(amount_disbursed=Sum('amount_disbursed'))

            amount_owed = UserLoan.objects.filter(
            active = True,
            paid = False,
            loan_request_status__in =loan_statuses
            ).aggregate(amount_left=Sum('amount_left'))
        

        metrics = {**amount_disbursed, **amount_owed, **amount_requested}
        return Response({"status":True, "detail":{"users":client_data, "metrics":metrics, "user_count":all_clients.count()} }, status.HTTP_200_OK)





# view to list out all debtors 
class DebtorsApiView(APIView):
    permission_classes = (IsAuthenticated,)
    mocked = False
    def get(self, request, *args, **kwargs):
        query_param = request.GET.get('query')
        if query_param is not None:
            all_debtors = UserLoan.objects.filter(active = True,
            paid = False,
            loan_request_status =constants.DISBURSED).filter(Q(user__first_name__icontains=query_param) | Q(user__last_name__icontains=query_param))
        else:
            all_debtors = UserLoan.objects.filter(active = True, paid = False, loan_request_status =constants.DISBURSED)
        serializer = serializers.DebtorsListSerializer(all_debtors, many=True)
        return Response({"status":True, "detail":serializer.data}, status.HTTP_200_OK)




# list to list our all pending loan applications 
class ApplicationApiView(APIView):
    permission_classes = (IsAuthenticated,)
    mocked = False
    def get(self, request, *args, **kwargs):
        query_param = request.GET.get('query')
        if query_param is not None:
            all_applications = UserLoan.objects.filter(active = True, paid = False, loan_request_status =constants.PENDING).filter(Q(user__first_name__icontains=query_param) | Q(user__last_name__icontains=query_param))
        else:
            all_applications = UserLoan.objects.filter(active = True, paid = False, loan_request_status =constants.PENDING)
        serializer = serializers.DebtorsListSerializer(all_applications, many=True)
        return Response({"status":True, "detail":serializer.data}, status.HTTP_200_OK)




# queryset = MyModel.objects.all()
# query = Q()
# for filter in filters:
#     query &= Q(**{filter['field_name']: filter['value']})
# queryset = queryset.filter(query)




class LoanStatusListView(APIView):
    # http://localhost:8001/example/?param1=value1&param2=value2
    # ?status=approved&total=1000
    # http://127.0.0.1:8001/api/v1/admin/loan-list/?status=approved&total=1000/

    serializer_class = serializers.LoanListSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request, status=None, total=None, **kwargs):
        paginator = PageNumberPagination()
        total = request.GET.get('total',10)
        statuss = request.GET.get('status', '')
        available_status = ["PENDING", "DISBURSED", "LATE", "SETTLED", "DISAPPROVED", "APPROVED"]
        try:
            int(total)
        except Exception as e:
            return Response({"detail":"total must be an integer", "status":True}, status.HTTP_200_OK)
        paginator.page_size = total

        if statuss:
            if statuss.upper() in available_status:
                loans = UserLoan.objects.filter(loan_request_status =constants.PENDING)
                result_page = paginator.paginate_queryset(loans, request)
                serializer = serializers.LoanListSerializer(result_page, many=True)
                return paginator.get_paginated_response({"status":True, "detail":serializer.data}, status.HTTP_200_OK)

        # return paginator.get_paginated_response({"status":False, "detail":"invalid status passed"}, status.HTTP_400_BAD_REQUEST)
        return paginator.get_paginated_response({"status":False, "detail":"invalid status passed"})

        
                