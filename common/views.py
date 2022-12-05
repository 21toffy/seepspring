from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (TestimonialListSerializer, OurTeamListSerializer)

from .models import(
    Testimonial, OurTeam
)


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




