
from django.urls import path
from .views import (
    ActiveLoanListView,
    InterestBreakdownView,
    GuarnteeListView,
HomePageListView,
    LoanPurposeListView,
    RepayLoan,
RepaymentGuideListView,
RequestLoan,
LoanLevelListView,
UserLoanRequestsListView,
SinglePromotionDetailView

)

app_name = 'loan'
urlpatterns = [
    path('active-loans-list', ActiveLoanListView.as_view(), name = 'active_loans'),
    path('interest-breakdown-view', InterestBreakdownView.as_view(), name = 'active_loans'),
    path('our-guarantee-list', GuarnteeListView.as_view(), name = 'our_guarantee_list'),
    path('homepage-list', HomePageListView.as_view(), name = 'homepage_list'),
    path('repayment-guide-list', RepaymentGuideListView.as_view(), name = 'repayment_guide_list'),
    path('loan-purpose-list', LoanPurposeListView.as_view(), name = 'loan_purpose_list'),
    path('request-for-loan', RequestLoan.as_view(), name='request-for-loan'),
    path('repay-loan', RepayLoan.as_view(), name='repay-loan'),
    path('loan-level', LoanLevelListView.as_view(), name='loan_level'),
    path('loan-request-list/', UserLoanRequestsListView.as_view(), name='loan_request'),

    path('single-promotion/', SinglePromotionDetailView.as_view(), name='single_promotion'),


]




# HomePageListView RepaymentGuideListView