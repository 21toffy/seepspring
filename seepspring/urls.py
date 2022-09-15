
from django.contrib import admin
from .views import home_page, populate_banks
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('', home_page, name="home-page"),
    path('populate', populate_banks, name="populate-banks"),
    path('api/v1/nigerian-banks/', include("banks.urls")),
    path('api/v1/loans/', include("loan.urls")),
    path('api/v1/admin/', include("adminapp.urls"))


]