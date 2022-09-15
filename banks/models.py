from django.db import models

from common.models import BaseModel

# Create your models here.


class NigerianBanks(BaseModel):
    bank_code = models.CharField(max_length=225, null=True, blank=True)
    bank_name = models.CharField(max_length=225, null=True, blank=True)
    def __str__(self):
        return self.bank_name
