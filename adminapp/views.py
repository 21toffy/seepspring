from datetime import datetime
from django.shortcuts import render

from accounts.models import CustomUser
from loan.models import UserLoan
from . import serializers

from common import constants
from common.utils import todays_date

from django.db.models import Q



from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,AllowAny)
from decimal import *
from django.db.models import Sum
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination




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

        if days is not 'all':
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

        
                