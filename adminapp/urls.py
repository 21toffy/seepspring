
from django.urls import path
from .views import (
AdminDashboard,
ApplicationApiView,
DebtorsApiView, 
AdminLoginAPIView,
LoanStatusListView,
ClientListAPIView,
LoanApplicationListAPIView,
LoanRepaymentListAPIView,
AmountDisbursedListAPIView,
PendingListAPIViewListAPIView,
UserLoanDetailView,
EmployeeCreation,
DepartmentListAPIView,
RoleListAPIView,
)

from rest_framework_simplejwt.views import TokenRefreshView



app_name = 'seepspring_adminapp'
urlpatterns = [
    path('admin-dashboard/<str:filter>',AdminDashboard.as_view(), name='admin_dashboard'),
    path('debtors-list',DebtorsApiView.as_view(), name='debtors-list-view'),
    path('applications-list',ApplicationApiView.as_view(), name='application-list-view'),
    path('login', AdminLoginAPIView.as_view(), name="login"),
    # path('loan-list/<str:status>/?<int:total>/?',LoanStatusListView.as_view(), name='loan-list-view'),
    path('loan-list/<str:status>/<int:total>',LoanStatusListView.as_view(), name='loan-list-view'),    
    path('clients-list', ClientListAPIView.as_view(), name='client_list'),
    path('loan-application-list', LoanApplicationListAPIView.as_view(), name='loanapplication_list'),
    path('loan-repayment-list', LoanRepaymentListAPIView.as_view(), name='loan_replay_list'),
    path('loan-disbursed-list', AmountDisbursedListAPIView.as_view(), name='loan_disbursed_list'),
    path('pending-loan-list', PendingListAPIViewListAPIView.as_view(), name='pending_loan_list'),
    path('employee-creation', EmployeeCreation.as_view(), name='employee-creation'),

    path('loan-details/<str:pk>/', UserLoanDetailView.as_view(), name='user_loan_detail'),

    path('departments/', DepartmentListAPIView.as_view(), name='department-list'),
    path('roles/', RoleListAPIView.as_view(), name='role-list'),



 

]

