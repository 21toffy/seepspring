
from django.urls import path
from .views import (
    ChangePasswordView,
    UserLoanProfileAPIView,
    UserProfileAPIView,
    UserRegistration,
    EmploymentDurationListView,
    SalaryRangeListView,

    LoginAPIView,
LogoutAPIView,
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
    path("loan-profile", UserLoanProfileAPIView.as_view(), name="loan-profile")


    



]
