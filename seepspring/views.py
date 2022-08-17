from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes

from accounts.models import CustomUser


@api_view(('GET',))
def home_page(request):
    users = CustomUser.objects.all()
    return Response({"message":"Hello World!, I think the DB was set up properly"})