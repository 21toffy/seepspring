from .models import (
NigerianBanks
)
from rest_framework import serializers

from accounts.models import CardCharge



class PaymentInitializerSerializer(serializers.Serializer):
    amount = serializers.FloatField(required=True)




class CardSerializer(serializers.Serializer):
    reference = serializers.CharField(max_length=100)
    card_number = serializers.CharField(max_length=16)
    cvv = serializers.CharField(max_length=4)
    expiry_month = serializers.CharField(max_length=2)
    expiry_year = serializers.CharField(max_length=4)
    email = serializers.EmailField()



class CardChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardCharge
        fields = '__all__'


class CardDetailsSerializer (serializers.ModelSerializer):
    class Meta:
        model = CardCharge
        fields = '__all__'


class NigerianBanksSerializer(serializers.ModelSerializer):

    class Meta:
        model = NigerianBanks


        fields = [
            "bank_code",
            "bank_name",
            "id",
        ]