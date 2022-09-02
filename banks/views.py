from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics



from .serializers import (
NigerianBanksSerializer

)

from .models import (
    NigerianBanks
)



class NigerianBanksListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NigerianBanksSerializer

    def get(self, request):
        nigerian_banks = NigerianBanks.objects.all()
        serializer = self.serializer_class(nigerian_banks, many=True)
        return Response({"details":"success", "data":serializer.data, "status":status.HTTP_200_OK}, status.HTTP_200_OK)
   