
from django.urls import path
from .views import (
    NigerianBanksListView

)

from rest_framework_simplejwt.views import TokenRefreshView



app_name = 'nigerian_banks'
urlpatterns = [
    path('list',NigerianBanksListView.as_view(), name='list_of_nigerian_banks'),


]
