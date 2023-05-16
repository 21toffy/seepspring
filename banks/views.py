from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from common.utils import (custom_serializer_error)



from .serializers import (
NigerianBanksSerializer,
CardDetailsSerializer,
CardChargeSerializer,
CardSerializer,
PaymentInitializerSerializer
)

from .models import (
    NigerianBanks,
    PaymentTrackingModel
)

from common.managers.paystack_manager import PaystackHandler

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from paystackapi.paystack import Paystack
from accounts.models import CardDetails, CardCharge
import uuid
from django.http import HttpResponse
import hashlib
# from .models import PaymentStatus, User, Card
# from .serializers import CardSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest
from accounts.models import CustomUser
from django.conf import settings
import requests

class InitTransaction(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, format=None):
        try:
            email = request.data['email']
            package_id = request.data['packageId']
            amount = request.data['amount']
            # first_name = package_id

            user = get_object_or_404(CustomUser, email=email)

            payload = {
                'email': email,
                'amount': amount,
            }

            headers = {
                'Accept': 'application/json,text/plain,/',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + settings.PAYSTACK_API_KEY,
            }

            response = requests.post(
                'https://api.paystack.co/transaction/initialize',
                headers=headers,
                json=payload,
            )

            data = response.json()
            print(data, 1234)
            return Response(data)

        except (KeyError, ValueError, TypeError):
            return HttpResponseBadRequest('Invalid input.')
        except (CustomUser.DoesNotExist):
            return Response({'message': 'User not found.'}, status=403)
        except Exception as e:
            return Response({'error': str(e), 'message': 'Error initializing transaction.'}, status=403)

class PayStackWebHook(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        # validate event
        # hashed_payload = hashlib.sha512(settings.PAYSTACK_API_KEY.encode('utf-8') + request.body.encode('utf-8')).hexdigest()
        hashed_payload = hashlib.sha512(settings.PAYSTACK_API_KEY.encode('utf-8') + request.body).hexdigest()
        print(hashed_payload)
        print(request.headers['x-paystack-signature'], "ddsssss")
        # hashed_payload = hashlib.sha512(settings.PAYSTACK_API_KEY + request.body).hexdigest()

        if hashed_payload == request.headers['x-paystack-signature']:
            mock =  True
        else:
            mock =  True
            # mock = False

        if mock:
            # Retrieve the request's body
            body = request.data
            if body['event'] == 'charge.success':
                # Do something with event
                data = body['data']
                authorization = data['authorization']
                customer = data['customer']
                # email = customer['email'].split('?')[1]
                email = customer['email']
                # package_id = customer['email'].split('?')[0]
                user = CustomUser.objects.filter(email=email).first()
                if user:
                    CardDetails.objects.create(
                        last4digits=authorization['last4'],
                        expiry_month=authorization['exp_month'],
                        expiry_year=authorization['exp_year'],
                        brand=authorization['brand'],
                        authorization_code=authorization['authorization_code'],
                        channel=authorization['channel'],
                        reusable=authorization['reusable'],
                        country_code=authorization['country_code'],
                        card_bank=authorization['bank'],
                        signature=authorization['signature'],
                        card_name=authorization['account_name'],
                        bin=authorization['bin'],
                        card_type=authorization['card_type'],
                        user=user,
                        is_active=True
                    )
                    return Response({"detail":"user does not exist", "status":False},status=status.HTTP_200_OK)
                return Response({"detail":"user does not exist", "status":False}, status.HTTP_400_BAD_REQUEST)
            return Response({"detail":"Charge not successful", "status":False}, status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"Invalid header", "status":False}, status.HTTP_400_BAD_REQUEST)


# class PayStackWebHook(APIView):


#     def post(self, request):
#         # validate event
#         hashed_payload = hashlib.sha512(settings.PAYSTACK_API_KEY + request.body).hexdigest()
#         if hashed_payload == request.headers['x-paystack-signature']:
#             # Retrieve the request's body
#             body = request.data
#             if body['event'] == 'charge.success':
#                 # Do something with event
#                 data = body['data']
#                 authorization = data['authorization']
#                 customer = data['customer']
#                 # email = customer['email'].split('?')[1]
#                 email = customer['email']
#                 package_id = customer['email'].split('?')[0]
#                 user = CustomUser.objects.filter(email=email).first()
#                 if user:
#                     CardDetails.objects.create(
#                         last4digits=authorization['last4'],
#                         expiry_month=authorization['exp_month'],
#                         expiry_year=authorization['exp_year'],
#                         brand=authorization['brand'],
#                         authorization_code=authorization['authorization_code'],
#                         channel=authorization['channel'],
#                         reusable=authorization['reusable'],
#                         country_code=authorization['country_code'],
#                         card_bank=authorization['bank'],
#                         signature=authorization['signature'],
#                         card_name=authorization['account_name'],
#                         bin=authorization['bin'],
#                         card_type=authorization['card_type'],
#                         user=user
#                     )
#                     return Response(status=status.HTTP_200_OK)
#                 return Response({"detail":"user does not exist", "status":False}, status.HTTP_400_BAD_REQUEST)
                



class InitiatlizePaystackTransactionView(APIView):
    """
    INITIALIZE A PAYSTACK TRANSACTION
    params:
        amount:
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PaymentInitializerSerializer(data=request.data)
        if serializer.is_valid():
            amount = float(request.data["amount"]) * 100
            reference = str(uuid.uuid4())

            res = PaystackHandler.initialize(reference, amount, request.user.email)

            if res["status"]:
                resp = {"detail": res['data'], "status": True}
                PaymentTrackingModel.objects.create(
                reference=reference,
                source="Initialize Charge Card",
                response_data=res,
                payment_status=True,
                amount=amount,
                )
                return Response(resp, status=status.HTTP_200_OK)
            else:
                resp = {"detail": res["message"], "status": False}
                return Response(
                    resp, status=status.HTTP_400_BAD_REQUEST
                )
        res = {"detail": custom_serializer_error(serializer.errors), "status": False}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)



class CardDetailsAPIView(APIView):
    def post(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():

            paystack = PaystackHandler()

            card_number=serializer.validated_data["card_number"]
            cvv=serializer.validated_data["cvv"]
            expiry_month=serializer.validated_data["expiry_month"]
            expiry_year=serializer.validated_data["expiry_year"]
            email=serializer.validated_data["email"]
            reference = serializer.validated_data["reference"]

            # Tokenize the card
            card_response = paystack.addCard(
                request.user,
                reference
            )
            # {'status': True, 'message': 'Authorization URL created', 'data': {'authorization_url': 'https://checkout.paystack.com/2h6yl0cq4qyee4z', 'access_code': '2h6yl0cq4qyee4z', 'reference': '18356511-5949-4b1a-805c-a06cfe6c4258'}}
            
            if card_response["status"]:
                print(card_response,"vvvvvvvvvvvs")

                # print(card_response)

                # # Save the card details
                # card_details = CardDetails(
                #     user=request.user,
                #     card_no=card_number,
                #     email=email,
                #     card_name=request.data.get('card_name'),
                #     card_bank=token['card']['bank'],
                #     last4digits=token['card']['last4digits'],
                #     authorization_email=token['authorization']['email'],
                #     expiry_month=expiry_month,
                #     expiry_year=expiry_year,
                #     card_type=token['card']['type'],
                #     authorization_code=token['authorization']['authorization_code'],
                #     is_active=True,
                #     is_primary=request.data.get('is_primary')
                # )
                # card_details.save()

                # serializer = CardDetailsSerializer(card_details)

                return Response({"details":card_response["data"], "status":True} , status=status.HTTP_201_CREATED)
            else:
                return Response({"details":card_response["message"], "message":card_response["message"], "status":False}, status=status.HTTP_400_BAD_REQUEST)


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardChargeAPIView(APIView):
    def post(self, request):
        paystack = PaystackHandler()
        card = CardDetails.objects.get(id=request.data.get('card_id'))

        # Charge the card
        reference = paystack.charge_card(
            card_number=card.card_no,
            cvv=card.cvv,
            expiry_month=card.expiry_month,
            expiry_year=card.expiry_year,
            amount=request.data.get('amount'),
            email=card.email
        )

        # Save the card charge details
        card_charge = CardCharge(
            reference=reference,
            card=card
        )
        card_charge.save()

        return Response({'reference': reference}, status=status.HTTP_201_CREATED)




class NigerianBanksListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = NigerianBanksSerializer

    def get(self, request):
        nigerian_banks = NigerianBanks.objects.all()
        serializer = self.serializer_class(nigerian_banks, many=True)
        return Response({"details":"success", "data":serializer.data, "status":True}, status.HTTP_200_OK)
   