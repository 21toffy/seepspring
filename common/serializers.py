from common.models import (Testimonial, OurTeam)
from rest_framework import serializers





class TestimonialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [  "image_url","person_name",
                    "testimony"]





class OurTeamListSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurTeam
        fields = [  "image_url","person_name",
                    "position"]




