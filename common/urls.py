
from django.urls import path
from .views import (
TestimonialApiView,
OurTeamApiView,
BannerView,
)



app_name = 'common'
urlpatterns = [
    path('testimonial',TestimonialApiView.as_view(), name='testimonial'),
    path('our-team',OurTeamApiView.as_view(), name='our-team'),
    path('banner',BannerView.as_view(), name='our-team'),

]
