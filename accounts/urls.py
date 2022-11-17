
from django.urls import path

from accounts.serializers import AdminLoginSerializer
from .views import (
    ChangePasswordView,
    CustomToken,
    GenerateOtpView,
    UserLoanProfileAPIView,
    UserProfileAPIView,
    UserRegistration,
    EmploymentDurationListView,
    SalaryRangeListView,
    SendOTPToPhone,
    ResolveBVN,
    LoginAPIView,
    LogoutAPIView,
    VerifyAccountNumber,
    VerifyPhone,
    UserMinimalProfileAPIView,
    UserBankAccountCreateView,
    UserBankAccountListView
)

from rest_framework_simplejwt.views import TokenRefreshView



app_name = 'accounts'
urlpatterns = [
    path('register',UserRegistration.as_view(), name='register'),
    path('login', LoginAPIView.as_view(), name="login"),
    # path('register/', RegisterView.as_view(), name="register"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),


    path('employment-durations',EmploymentDurationListView.as_view(), name='employment-durations'),
    path('salary-ranges',SalaryRangeListView.as_view(), name='salary-ranges'),

    # path("change-password/<uuid:pk>", ChangePasswordView.as_view(), name="change-password")
    path("change-password", ChangePasswordView.as_view(), name="change-password"),
    path("me", UserProfileAPIView.as_view(), name="profile"),
    path("loan-profile", UserLoanProfileAPIView.as_view(), name="loan-profile"),

    path("generate", GenerateOtpView.as_view(), name="generate-otp"),

    path("verify-token", CustomToken.as_view(), name="admin-login"),


    path("verify-account-number", VerifyAccountNumber.as_view(), name="verify_account_number"),

    path("send-otp", SendOTPToPhone.as_view(), name="send_phone_number"),


    path("verify-otp", VerifyPhone.as_view(), name="verify_otp"),

    path("fetch-bvn/<str:bvn>", ResolveBVN.as_view(), name="verify_otp"),
    path("user/profile", UserMinimalProfileAPIView.as_view(), name="loan-profile"),


    path("create-bank-account", UserBankAccountCreateView.as_view(), name="create_bank_account"),

    path("list-bank-account", UserBankAccountListView.as_view(), name="list_bank_account"),


]
