from datetime import datetime
from django.shortcuts import render
from .models import (Interest, InterestBreakdown, LoanLevel, LoanPurpose, UserLoan, HomePagePromotion, Guarntee,
RepaymentGuide,
)
from .serializers import (LoanRequestSerializer, RepaymentGuideSerializer, UserLoanserializer, InterestBreakdownSerializer, InterestSerializer, RepaymentGuideSerializer,
HomePagePromotionSerializer,
GuarnteeSerializer,
loanPurposeserializer,
)
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,AllowAny)
from decimal import *
from django.db import transaction



# Create your views here.


class RequestLoan(APIView):
    # serializer_class = GuarnteeSerializer
    permission_classes = (IsAuthenticated,)

    def get_loan_eligibility_details(self,):
        with transaction.atomic():
            import datetime
            todays_date = datetime.date.today()
            loan_exists = UserLoan.objects.filter(active=True, paid=False).first()
            if loan_exists:
                default_delta = todays_date - loan_exists.loan_due_date
                default_days = default_delta.days
                return False
            return True
    def post(self, request, *args, **kwargs):
        with transaction.atomic():         
            if self.get_loan_eligibility_details() is True:
                serializer = LoanRequestSerializer(data=request.data)
                if serializer.is_valid():
                    user = request.user
                    validated_data = serializer.validated_data
                    loan_purpose = validated_data.get("loan_purpose")
                    interest = validated_data.get("interest")
                    amount = validated_data.get("amount")
                    try:
                        loan_purpose_obj = LoanPurpose.objects.get(id=loan_purpose)
                        interest_obj = Interest.objects.filter(id=interest).first()
                        loan_level_obj = LoanLevel.objects.filter(level=user.user_level).first()
                    except Exception as does_not_exist:
                        return Response(str(does_not_exist),{"message":"failed", "status":status.HTTP_404_NOT_FOUND},status= status.HTTP_404_NOT_FOUND) 

                    user_loan = UserLoan.objects.create(
                        loan_purpose = loan_purpose_obj,
                        user=user,
                        interest =interest_obj,
                        loan_level = loan_level_obj,
                        amount_requested = Decimal(amount) * 100
                    )
                    data = {
                        "id": user_loan.id,
                        "requested_amount": user_loan.amount_requested/100,
                        "disbursed_amount": user_loan.amount_disbursed/100,
                        "due_date": user_loan.loan_due_date,
                        "purpose": user_loan.loan_purpose.purpose,

                    }
                    return Response({"message":"success", "data":data, "status":status.HTTP_200_OK},status= status.HTTP_200_OK)
                else:
                    return Response(serializer.errors,{"message":"failed", "status":status.HTTP_400_BAD_REQUEST},status= status.HTTP_400_BAD_REQUEST)       
            else:
                return Response({"message":"You are not eligible for a loan", "data":{}, "status":status.HTTP_400_BAD_REQUEST}, status= status.HTTP_400_BAD_REQUEST)



class LoanPurposeListView(APIView):
    serializer_class = loanPurposeserializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            loan_purposes = LoanPurpose.objects.filter(active=True)
            serializer = self.serializer_class(loan_purposes, many=True)
            return Response({"message":"success", "data":serializer.data, "status":status.HTTP_200_OK},status= status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)




class GuarnteeListView(APIView):
    serializer_class = GuarnteeSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            our_guarantee = Guarntee.objects.filter(active=True)
            serializer = self.serializer_class(our_guarantee)
            return Response({"message":"success", "data":serializer.data, "status":status.HTTP_200_OK},status= status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)




class HomePageListView(APIView):
    serializer_class = HomePagePromotionSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            home_page_promotion = HomePagePromotion.objects.filter(active=True).first()
            serializer = HomePagePromotionSerializer(home_page_promotion)
            return Response({"message":"success", "data":serializer.data, "status":status.HTTP_200_OK},status= status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)




class RepaymentGuideListView(APIView):
    serializer_class = RepaymentGuideSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            repayment_guide = RepaymentGuide.objects.filter(active=True)
            serializer = self.serializer_class(repayment_guide, many=True)
            return Response({"message":"success", "data":serializer.data, "status":status.HTTP_200_OK},status= status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={}, status=status.HTTP_400_BAD_REQUEST)




class ActiveLoanListView(APIView):
    serializer_class = UserLoanserializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        active_user_loans = UserLoan.objects.filter(active=True).order_by("-created_at")[:5]
        serializer = self.serializer_class(active_user_loans, many=True)
        return Response({"message":"success", "data":serializer.data, "status":status.HTTP_200_OK},status= status.HTTP_200_OK)
        



class InterestBreakdownView(APIView):
    InterestSerializer
    serializer_class = InterestBreakdownSerializer
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            active_interest = Interest.objects.filter(active=True).first()
            all_interest_breakdown = InterestBreakdown.objects.all().first()
        except Exception as e:
            return Response({"data":{}}, status=status.HTTP_400_BAD_REQUEST)

        active_interest_serializer = {
            "id":active_interest.id,
            "interest_name":active_interest.interest_name,
            "vat":active_interest.vat,
            "service_charge":active_interest.service_charge,
            "interest":active_interest.interest,
        }


        all_interest_breakdown_serializer = {
            "id":all_interest_breakdown. id,
            "text_1":all_interest_breakdown.text_1,
            "text_2":all_interest_breakdown.text_2,
            "text_4":all_interest_breakdown.text_4,
            "text_5":all_interest_breakdown.text_5,
            "text_6":all_interest_breakdown.text_6,
            "text_7":all_interest_breakdown.text_7,
            "text_8":all_interest_breakdown.text_8,
            "text_9":all_interest_breakdown.text_9,
            "text_10":all_interest_breakdown.text_10,
        }
        res={
            "active_interest":active_interest_serializer,
            "interest_break_down":all_interest_breakdown_serializer
        }

        return Response({"message":"success", "data":res, "status":status.HTTP_200_OK},status= status.HTTP_200_OK)
