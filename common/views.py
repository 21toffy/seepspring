from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (TestimonialListSerializer, OurTeamListSerializer)
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from .models import(
    Testimonial, OurTeam, Banner
)




class BannerView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        try:
            banner = Banner.objects.filter(active = True).first()
            if banner is not None:

                response_data = {
                "status": True,
                "detail": {
                    "title": banner.title,
                    "subtitle": banner.subtitle,
                    "image": banner.image_url,
                }
                }
                return Response(response_data, status.HTTP_200_OK)
            else:
                response_data = {
                "status": False,
                "detail": {
                    "title": "",
                    "subtitle": "",
                    "image": "",
                }
                }
                return Response(response_data, status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"status":False, "detail":str(e)}, status.HTTP_400_BAD_REQUEST)




class BannerDetailView(DetailView):
    model = Banner
    

    def get(self, request, *args, **kwargs):

        try:
            banner = self.get_object()
        except ObjectDoesNotExist:
            return JsonResponse({"status": False, "detail": {}}, status=status.HTTP_400_BAD_REQUEST)
        
        response_data = {
            "status": True,
            "detail": {
                "title": banner.title,
                "subtitle": banner.subtitle,
                "image": banner.image_url,
            }
        }
        
        return JsonResponse(response_data, status=status.HTTP_200_OK)



class TestimonialApiView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        try:
            testimonial = Testimonial.objects.filter(active = True)
            serializer = TestimonialListSerializer(testimonial, many=True)
            return Response({"status":True, "detail":serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":False, "detail":str(e)}, status.HTTP_200_OK)


class OurTeamApiView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        try:
            our_team = OurTeam.objects.filter(active = True)
            serializer = OurTeamListSerializer(our_team, many=True)
            return Response({"status":True, "detail":serializer.data}, status.HTTP_200_OK)
        except Exception as e:
            return Response({"status":False, "detail":str(e)}, status.HTTP_200_OK)




