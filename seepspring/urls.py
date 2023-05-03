
from django.contrib import admin
from .views import home_page, populate_banks, populate_user
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('', home_page, name="home-page"),
    path('populate', populate_banks, name="populate-banks"),
    
    path('populate-users', populate_user, name="populate-user"),

    
    path('api/v1/nigerian-banks/', include("banks.urls")),
    path('api/v1/loans/', include("loan.urls")),
    path('api/v1/admin/', include("adminapp.urls")),
    path('api/v1/common/', include("common.urls")),
    path('api/v1/banks/', include("banks.urls"))

]