from datetime import datetime
from django.shortcuts import render

from accounts.models import CustomUser
from loan.models import UserLoan
from . import serializers

from common import constants
from common.utils import todays_date

from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,AllowAny)
from decimal import *
from django.db.models import Sum


class AdminDashboard(APIView):
    permission_classes = (IsAuthenticated,)
    mocked = False
    def get(self, request, *args, **kwargs):
        all_clients = CustomUser.objects.filter(is_staff=False)
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
                "emergency_contact_relationship":client.emergencycontact_set.first().relationship,
                "emergency_contact_name":client.emergencycontact_set.first().name,
                "emergency_contact_phone_number":client.emergencycontact_set.first().phone_number,
                "colleague_contact_name":client.colleaguecontact_set.first().name,
                "colleague_contact_phone_number":client.colleaguecontact_set.first().phone_number,
            }
            client_data.append(client_dict)
        loan_statuses = [constants.DISBURSED, constants.LATE, constants.PART_SETTLEMENT]
        amount_requested = UserLoan.objects.filter(active = True, paid = False, loan_request_status__in =loan_statuses).aggregate(amount_requested=Sum('amount_requested'))
        amount_disbursed =  UserLoan.objects.filter(active = True, paid = False, loan_request_status__in =loan_statuses).aggregate(amount_disbursed=Sum('amount_disbursed'))
        amount_owed = UserLoan.objects.filter(active = True, paid = False, loan_request_status__in =loan_statuses).aggregate(amount_left=Sum('amount_left'))
        metrics = {**amount_disbursed, **amount_owed, **amount_requested}
        return Response({"detail":"success", "status":status.HTTP_200_OK, "data":{"users":client_data, "metrics":metrics} }, status.HTTP_200_OK)




class DebtorsApiView(APIView):
    permission_classes = (IsAuthenticated,)
    mocked = False
    def get(self, request, *args, **kwargs):
        all_debtors = UserLoan.objects.filter(active = True, paid = False, loan_request_status =constants.DISBURSED)
        serializer = serializers.DebtorsListSerializer(all_debtors, many=True)
        return Response({"detail":"success", "status":status.HTTP_200_OK, "data":serializer.data}, status.HTTP_200_OK)




class ApplicationApiView(APIView):
    permission_classes = (IsAuthenticated,)
    mocked = False
    def get(self, request, *args, **kwargs):
        all_debtors = UserLoan.objects.filter(active = True, paid = False, loan_request_status =constants.PENDING)
        serializer = serializers.DebtorsListSerializer(all_debtors, many=True)
        return Response({"detail":"success", "status":status.HTTP_200_OK, "data":serializer.data}, status.HTTP_200_OK)
