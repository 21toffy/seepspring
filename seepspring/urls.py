
from django.contrib import admin
from .views import home_page
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('accounts.urls')),
    path('', home_page, name="home-page")


]