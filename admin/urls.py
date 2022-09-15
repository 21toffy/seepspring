
from django.urls import path
from .views import (
AdminDashboard,
ApplicationApiView,
DebtorsApiView, 
)

from rest_framework_simplejwt.views import TokenRefreshView



app_name = 'seepspring_admin'
urlpatterns = [
    path('admin-dashboard',AdminDashboard.as_view(), name='admin_dashboard'),
    path('debtors-list',DebtorsApiView.as_view(), name='debtors-list-view'),
    path('applications-list',ApplicationApiView.as_view(), name='application-list-view'),


]
