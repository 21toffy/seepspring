from datetime import datetime
from django.shortcuts import render

from accounts import serializers
from common import constants
from common.utils import todays_date
import loan
from .models import (Interest, InterestBreakdown, LoanLevel, LoanPurpose, UserLoan, HomePagePromotion, Guarntee,
RepaymentGuide,LoanPageInformationSlider, SinglePromotion, BankAccountDetails
)
from .serializers import (LoanLevelserializer, LoanRepaymentSerializer, LoanRequestSerializer, RepaymentGuideSerializer, UserLoanserializer, InterestBreakdownSerializer, InterestSerializer, RepaymentGuideSerializer,
HomePagePromotionSerializer,
GuarnteeSerializer,
loanPurposeserializer,LoanPageInformationSliderSerializer,
SinglePromotionSerializer,
)
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,AllowAny)
from decimal import *
from django.db import transaction
from common.utils import get_first_serializer_error



# Create your views here.



class SinglePromotionDetailView(APIView):
    serializer_class = SinglePromotionSerializer
    permission_classes = (AllowAny,)
    def get(self, request):
        single_promotion = SinglePromotion.objects.filter(active = True).first()
        # if single_promotion is None:
        #     return Response({"detail":{}, "status":True}, status.HTTP_200_OK)
        serializer = self.serializer_class(single_promotion)
        return Response({"detail":serializer.data, "status":True}, status.HTTP_200_OK)

class LoanLevelListView(APIView):
    serializer_class = LoanLevelserializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            user_level = request.user.user_level
            loan_level = LoanLevel.objects.filter(level = user_level).first()
            serializer = self.serializer_class(loan_level)
            return Response({"detail": serializer.data, "status":True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail":str(e), status:False}, status.HTTP_400_BAD_REQUEST)


class RepayLoan(APIView):
    # permission_classes = (IsAuthenticated,)
    
    mocked = False
    def post(self, request, *args, **kwargs):
        if self.mocked is True:
            pass
        else:
            loan_exists = UserLoan.objects.filter(active=True, paid=False).first()
            if loan_exists:
                serializer = LoanRepaymentSerializer(data=request.data)
                if serializer.is_valid():
                    repayment_instance = serializer.save()
                    amount_repayed = repayment_instance.amount
                    repayment_instance.user_loan = loan_exists
                    repayment_instance.save()
                    money_left = loan_exists.amount_left - Decimal(amount_repayed)
                    loan_exists.amount_left = Decimal(money_left)
                    if money_left <= 0:
                        loan_exists.paid = True
                        loan_exists.active = False
                        loan_exists.loan_repayment_status = constants.SETTLED
                        loan_exists.save()

                        if todays_date() > loan_exists.loan_due_date and loan_exists.number_of_default_days > 5:
                            loan_exists.paid_ontime = False
                            loan_exists.load_default.status =True
                            loan_exists.save()
                    else:
                        loan_exists.loan_repayment_status = constants.PART_SETTLEMENT
                        loan_exists.save()
                    data = {
                        "amount_payed" : serializer.validated_data["amount"],
                        "amount_left": Decimal(0) if money_left <= 0 else money_left,
                        "detail":loan_exists.get_loan_default_details
                    }
                    return Response({"detail":"success", "data":data, "status":True}, status.HTTP_200_OK)
                else:
                    return Response({"detail":serializer.errors, "status":False}, status.HTTP_400_BAD_REQUEST)

            else:
                return Response({"detail":"You dont have an outstanding loan", "data":{}, "status":False}, status.HTTP_400_BAD_REQUEST)



class RequestLoan(APIView):
    # serializer_class = GuarnteeSerializer
    # permission_classes = (IsAuthenticated,)

    def get_loan_eligibility_details(self,user):
        with transaction.atomic():
            import datetime
            todays_date = datetime.date.today()
            loan_exists = UserLoan.objects.filter(user=user, active=True, paid=False).first()
            if loan_exists:
                default_delta = todays_date - loan_exists.loan_due_date
                default_days = default_delta.days
                return False
            return True
    def post(self, request, *args, **kwargs):
        with transaction.atomic():         
            if self.get_loan_eligibility_details(request.user) is True:
                serializer = LoanRequestSerializer(data=request.data)
                if serializer.is_valid():
                    user = request.user
                    validated_data = serializer.validated_data
                    loan_purpose = validated_data.get("loan_purpose")
                    interest = validated_data.get("interest")
                    amount = validated_data.get("amount")
                    account_number = validated_data.get("account_number")                    
                    if Decimal(amount) > 5000000:
                        return Response({"detail":"you are not eligible for a loan above ₦ 50'000", "status":False}, status.HTTP_400_BAD_REQUEST)
                    if Decimal(amount) < 100000:
                        return Response({"detail":"you can not request for a loan below ₦ 1'000", "status":False}, status.HTTP_400_BAD_REQUEST)
                    try:
                        loan_level_obj = LoanLevel.objects.filter(level=user.user_level).first()
                        if Decimal(amount) > loan_level_obj.max_amount *100 :
                            return Response({"detail":f"you are not eligible for a loan above ₦ {float(loan_level_obj.max_amount)}", "status":False}, status.HTTP_400_BAD_REQUEST)
                        loan_purpose_obj = LoanPurpose.objects.get(id=loan_purpose)
                        interest_obj = Interest.objects.get(id=interest)
                        account_number_obj = BankAccountDetails.objects.get(id = account_number)
                    except Exception as does_not_exist:
                        return Response ({"detail":str(does_not_exist), "status":False}, status.HTTP_404_NOT_FOUND) 
                    user_loan = UserLoan.objects.create(
                        loan_purpose = loan_purpose_obj,
                        account_number = account_number_obj,
                        user=user,
                        interest =interest_obj,
                        loan_level = loan_level_obj,
                        amount_requested = Decimal(amount),
                        amount_left = Decimal(amount)
                    )
                    data = {
                        # "id": user_loan.id,
                        "requested_amount": user_loan.amount_requested,
                        "disbursed_amount": user_loan.amount_disbursed,
                        "due_date": user_loan.loan_due_date,
                        "purpose": user_loan.loan_purpose.purpose,

                    }
                    return Response({"detail":"loan request submitted and would be disbursed in a moment", "data":data, "status":True}, status.HTTP_200_OK)
                else:
                    return Response({"detail":get_first_serializer_error(serializer.errors), "status":False}, status.HTTP_400_BAD_REQUEST)       
            else:
                return Response({"detail":"You are not eligible for a loan", "status":False}, status.HTTP_200_OK)



class LoanPurposeListView(APIView):
    serializer_class = loanPurposeserializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            loan_purposes = LoanPurpose.objects.filter(active=True)
            serializer = self.serializer_class(loan_purposes, many=True)
            return Response({"detail":"success", "data":serializer.data, "status":True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail":str(e), "status":False}, status=status.HTTP_400_BAD_REQUEST)




class GuarnteeListView(APIView):
    serializer_class = GuarnteeSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            our_guarantee = Guarntee.objects.filter(active=True)
            serializer = self.serializer_class(our_guarantee)
            return Response({"detail":"success", "data":serializer.data, "status":True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail":str(e), "status":False}, status=status.HTTP_400_BAD_REQUEST)




class HomePageListView(APIView):
    serializer_class = HomePagePromotionSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            home_page_promotion = HomePagePromotion.objects.filter(active=True).first()
            serializer = HomePagePromotionSerializer(home_page_promotion)
            return Response({"detail":"success", "data":serializer.data, "status":True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail":str(e), "status":False}, status=status.HTTP_400_BAD_REQUEST)




class RepaymentGuideListView(APIView):
    serializer_class = RepaymentGuideSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            repayment_guide = RepaymentGuide.objects.filter(active=True)
            serializer = self.serializer_class(repayment_guide, many=True)
            return Response({"detail":"success", "data":serializer.data, "status":True}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail":str(e), "status":False}, status=status.HTTP_400_BAD_REQUEST)



class ActiveLoanListView(APIView):
    serializer_class = UserLoanserializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        active_user_loans = UserLoan.objects.filter(active=True).order_by("-created_at")[:5]
        serializer = self.serializer_class(active_user_loans, many=True)
        return Response({"detail":"success", "data":serializer.data, "status":True}, status.HTTP_200_OK)
        



from rest_framework.pagination import PageNumberPagination

# class UserLoanRequestsListView(APIView):
#     serializer_class = UserLoanserializer
#     permission_classes = (IsAuthenticated,)
#     def get(self, request, **kwargs):
#         paginator = PageNumberPagination()
#         total = request.GET.get('total',10)
#         statuss = request.GET.get('status', '')
#         available_status = ["PENDING", "DISBURSED", "LATE", "SETTLED", "DISAPPROVED", "APPROVED"]
#         try:
#             int(total)
#         except Exception as e:
#             return Response({"detail":"total must be an integer", "status":True}, status.HTTP_200_OK)
#         paginator.page_size = total

#         if statuss:
#             if statuss.upper() in available_status:
#                 active_user_loans = UserLoan.objects.filter(user= request.user, loan_request_status__exact = statuss.upper()).order_by("-created_at")
#             else:
#                 active_user_loans = UserLoan.objects.filter(user = request.user).order_by("-created_at")
#         else:
#             active_user_loans = UserLoan.objects.filter(user = request.user).order_by("-created_at")
#         result_page = paginator.paginate_queryset(active_user_loans, request)
#         serializer = UserLoanserializer(result_page, many=True)
#         return paginator.get_paginated_response(serializer.data) 


class UserLoanRequestsListView(APIView):
    serializer_class = UserLoanserializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        try:
            available_status = ["PENDING", "DISBURSED", "LATE", "SETTLED", "DISAPPROVED", "APPROVED"]
            active_user_loans = UserLoan.objects.filter(user=request.user).order_by("-created_at")
            serializer = UserLoanserializer(active_user_loans, many=True)
            response_data = {
                "status": True,
                "detail": serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "status": False,
                "detail": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            
            
        









class InterestBreakdownView(APIView):
    InterestSerializer
    serializer_class = InterestBreakdownSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            active_interest = Interest.objects.filter(active=True).first()
        except Exception as e:
            return Response({"data":{}}, status=status.HTTP_400_BAD_REQUEST)
        active_interest_serializer = {
            "id":active_interest.id,
            "interest_name":active_interest.interest_name,
            "vat":active_interest.vat,
            "service_charge":active_interest.service_charge,
            "interest":active_interest.interest,
        }
        loan_page_information_slider = LoanPageInformationSlider.objects.filter(interest = active_interest, active=True)
        serializer = LoanPageInformationSliderSerializer(loan_page_information_slider, many=True)
        res={
            "active_interest":active_interest_serializer,
            "active_loan_information_slider":serializer.data
        }
        return Response({"detail":res, "status":True}, status.HTTP_200_OK)
