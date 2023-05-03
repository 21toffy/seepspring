
from django.urls import path
from .views import (
    NigerianBanksListView,
    CardDetailsAPIView,
    CardChargeAPIView,
    InitiatlizePaystackTransactionView,
    PayStackWebHook
)

from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'nigerian_banks'
urlpatterns = [
    path('list',NigerianBanksListView.as_view(), name='list_of_nigerian_banks'),
    path('tokenize-add-card',CardDetailsAPIView.as_view(), name='tokenize_card'),
    path('initialize',InitiatlizePaystackTransactionView.as_view(), name='initialize-transaction'),
    path('charge-card',CardChargeAPIView.as_view(), name='charge_card'),
    path('webhook',PayStackWebHook.as_view(), name='webhook'),

    
]
