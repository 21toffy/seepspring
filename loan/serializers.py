from dataclasses import fields

from common import constants
from .models import (Interest, InterestBreakdown, LoanPurpose, UserLoan, HomePagePromotion, Guarntee,
RepaymentGuide,)
from rest_framework import serializers



class loanPurposeserializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPurpose
        fields= ["id", "purpose"]



class LoanRequestSerializer(serializers.Serializer):
    loan_purpose = serializers.UUIDField()
    interest = serializers.UUIDField()
    amount = serializers.DecimalField(default=0.0, decimal_places=constants.DECIMAL_PLACES, max_digits=constants.MAX_DIGITS)
    class Meta:
        fields= [
            "loan_purpose",
            "interest",
            "amount",
        ]


class RepaymentGuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepaymentGuide
        fields = "__all__"

class HomePagePromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePagePromotion
        fields = "__all__"

class GuarnteeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guarntee
        fields = "__all__"



class UserLoanserializer(serializers.ModelSerializer):
    class Meta:
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
  

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = (
            "id",
            "interest_name",
            "vat",
            "service_charge",
            "interest",
        )


class InterestBreakdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterestBreakdown
        fields = (
            "id",
            "text_1",
            "text_2",
            "text_4",
            "text_5",
            "text_6",
            "text_7",
            "text_8",
            "text_9",
            "text_10",

        )

