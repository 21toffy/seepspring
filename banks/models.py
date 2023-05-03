from django.db import models

from common.models import BaseModel

# Create your models here.


class NigerianBanks(BaseModel):
    bank_code = models.CharField(max_length=225, null=True, blank=True)
    bank_name = models.CharField(max_length=225, null=True, blank=True)
    def __str__(self):
        return self.bank_name

class PaymentTrackingModel(BaseModel):
    """
    Payment log model
    """

    reference = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=50)
    response_data = models.TextField(null=True)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        self.reference
