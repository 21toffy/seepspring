from .models import (
NigerianBanks
)
from rest_framework import serializers



class NigerianBanksSerializer(serializers.ModelSerializer):

    class Meta:
        model = NigerianBanks


        fields = [
            "bank_code",
            "bank_name",
            "id",
        ]