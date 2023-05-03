import uuid
from django.db.models import F
from django.db import transaction, IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
import requests
from accounts.models import CardDetails

from banks.models import PaymentTrackingModel



# paystack_secret_key = settings.PAYSTACK_API_KEY
# paystack = Paystack(secret_key=paystack_secret_key)



class PaystackHandler(object):
    BASE_URL = 'https://api.paystack.co'
    def __init__(self):
        # Initialize the Paystack API key
        self.api_key = settings.PAYSTACK_API_KEY

        # Create a requests session
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': 'Bearer ' + self.api_key,
            'Content-Type': 'application/json'
        })
    
    # class PaystackAPIError(Exception):
    #     @transaction.atomic
    #     pass

    @staticmethod
    def initialize(reference, amount, email):
        """
        initialize a paystack transaction
        """
        initializer_response = Transaction.initialize(
            reference=reference, amount=amount, email=email
        )
        return initializer_response

    # def paystackWithCard(amount, card, wallet_to):
    #     """
    #     Wallet funding using paystack tokenized card
    #     """


    #     # get user's card details
    #     try:
    #         user_card = CardModel.objects.get(card_id=card, user=wallet_to.user.id)
    #     except CardModel.DoesNotExist or KeyError or CardModel.MultipleObjectsReturned:
    #         # if card does not exit

    #         failover_expected["response"] = "Invalid card"
    #         PaymentFailOver.save_new_failover(failover_expected)
    #         track_user_activity.delay(
    #             action="Pay with card, invalid card",
    #             actor_email=wallet_to.user.email,
    #             context={
    #                 "wallet_to": str(wallet_to),
    #                 "card": str(card),
    #             },
    #         )
    #         return {"status": False, "error": "INVALID_CARD", "message": "Invalid Card"}

    #     # generate transaction reference
    #     transaction_ref = "CR" + uuid.uuid4().hex[:8]

    #     # debit users card
    #     debit_response = Transaction.charge(
    #         reference=transaction_ref,
    #         authorization_code=user_card.authorization_code,
    #         email=user_card.authorization_email,
    #         amount=int(amount) * 100,
    #     )

    #     if debit_response["status"] == False:
    #         return {"status": False, "message": debit_response["message"]}

    #     # if paystack transfer call is successful
    #     if debit_response["data"]["status"] != "failed":
    #         PaymentTrackingModel.objects.create(
    #             reference=transaction_ref,
    #             source="Charge Card",
    #             response_data=debit_response,
    #             payment_status=True,
    #             amount=amount,
    #         )

    #         initial_save_point = transaction.savepoint()
    #         try:
    #             with transaction.atomic():

    #                 # create credit transaction record
    #                 TransactionModel.objects.create(
    #                     reference="Cr" + uuid.uuid4().hex[:8],
    #                     user=wallet_to.user,
    #                     amount=amount,
    #                     status="2",
    #                     wallet=wallet_to,
    #                     type="Credit",
    #                     description="Credit",
    #                     category="WALLET_CREDIT",
    #                 )

    #                 # credit reciever's wallet
    #                 WalletModel.objects.filter(id=wallet_to.id).update(
    #                     balance=F("balance") + amount
    #                 )
    #                 track_user_activity.delay(
    #                     action="Pay with card, successful",
    #                     actor_email=wallet_to.user.email,
    #                     context={
    #                         "wallet_to": str(wallet_to),
    #                         "card": str(card),
    #                         "debit_response": debit_response["data"],
    #                     },
    #                 )
    #                 return {"status": True, "message": "Transaction Successful"}

    #         except (IntegrityError, DatabaseError, ObjectDoesNotExist, ValueError) as a:

    #             # TODO log error here

    #             PaymentTrackingModel.objects.create(
    #                 reference=transaction_ref,
    #                 source="Charge Card",
    #                 response_data=debit_response,
    #                 payment_status=False,
    #                 amount=amount,
    #             )

    #             transaction.savepoint_rollback(initial_save_point)

    #             failover_expected["response"] = "Server Error - {}".format(a)
    #             PaymentFailOver.save_new_failover(failover_expected)
    #             track_user_activity.delay(
    #                 action="Pay with card, Tramsaction failed",
    #                 actor_email=wallet_to.user.email,
    #                 context={
    #                     "wallet_to": str(wallet_to),
    #                     "card": str(card),
    #                     "error": str(a),
    #                 },
    #             )
    #             return {
    #                 "status": False,
    #                 "error": "SERVER_ERROR",
    #                 "message": "Transation failed....please contact admin",
    #             }

    #     else:
    #         failover_expected["response"] = debit_response["message"]
    #         PaymentFailOver.save_new_failover(failover_expected)
    #         track_user_activity.delay(
    #             action="Pay with card, Tramsaction failed",
    #             actor_email=wallet_to.user.email,
    #             context={
    #                 "wallet_to": str(wallet_to),
    #                 "card": str(card),
    #                 "error": debit_response["message"],
    #             },
    #         )
    #         return {
    #             "status": False,
    #             "error": "PAYMENT_ERROR",
    #             "message": debit_response["message"],
    #         }

    def _handle_error(self, response):
        # Handle API errors
        if response.status_code >= 400:
            error_msg = response.json()['message']
            raise self.PaystackAPIError(error_msg)


    def charge_card(self, card_number, cvv, expiry_month, expiry_year, amount, email):
        # Create a payload for charging the card
        payload = {
            'email': email,
            'amount': amount,
            'card': {
                'number': card_number,
                'cvv': cvv,
                'expiry_month': expiry_month,
                'expiry_year': expiry_year
            }
        }

        # Make a POST request to the Paystack charge endpoint
        url = self.BASE_URL + '/charge'
        response = self.session.post(url, json=payload)

        # Handle API errors
        self._handle_error(response)

        # Return the reference for the transaction
        response_json = response.json()
        return response_json['data']['reference']
    
    def tokenize_card(self, card_number, cvv, expiry_month, expiry_year):
        # Create a payload for tokenizing the card
        payload = {
            'card': {
                'number': card_number,
                'cvv': cvv,
                'expiry_month': expiry_month,
                'expiry_year': expiry_year
            }
        }

        # Make a POST request to the Paystack tokenize endpoint
        url = self.BASE_URL + '/v1/tokens'
        response = self.session.post(url, json=payload)


        # Handle API errors
        self._handle_error(response)

        # Return the token for the card
        response_json = response.json()
        return response_json['data']['token']
    
    @transaction.atomic
    def addCard(self, user, reference):
        """
        ADD A NEW CARD TO USER'S ACCOUNT
        """

        verify_response = Transaction.verify(reference=reference)
        print(verify_response, 345)

        # if paystack call is successful
        if verify_response["status"] == True:

            # {'status': True, 'message': 'Verification successful', 'data': {'id': 2721276222, 'domain': 'test', 'status': 'abandoned', 'reference': '4f7e94b7-03c5-4d99-a58b-e3afaa8bde80', 'amount': 300000, 'message': None, 'gateway_response': 'The transaction was not completed', 'paid_at': None, 'created_at': '2023-04-14T16:05:13.000Z', 'channel': 'card', 'currency': 'NGN', 'ip_address': '102.89.32.83, 162.158.38.226, 172.31.68.120', 'metadata': '', 'log': None, 'fees': None, 'fees_split': None, 'authorization': {}, 'customer': {'id': 119885614, 'first_name': None, 'last_name': None, 'email': 'okedejit@yahoo.com', 'customer_code': 'CUS_s82ve76zlb8fcn7', 'phone': None, 'metadata': None, 'risk_action': 'default', 'international_format_phone': None}, 'plan': None, 'split': {}, 'order_id': None, 'paidAt': None, 'createdAt': '2023-04-14T16:05:13.000Z', 'requested_amount': 300000, 'pos_transaction_data': None, 'source': None, 'fees_breakdown': None, 'transaction_date': '2023-04-14T16:05:13.000Z', 'plan_object': {}, 'subaccount': {}}}
            # extract need data from paysatack response
            last4digits = verify_response["data"]["authorization"]["last4"]
            authorization_email = verify_response["data"]["customer"]["email"]
            expiry_month = verify_response["data"]["authorization"]["exp_month"]
            expiry_year = verify_response["data"]["authorization"]["exp_year"]
            authorization_code = verify_response["data"]["authorization"][
                "authorization_code"
            ]
            card_type = verify_response["data"]["authorization"]["card_type"]
            bank = verify_response["data"]["authorization"]["bank"]
            reuseable = verify_response["data"]["authorization"]["reusable"]

            # add card
            try:
                card = CardDetails(
                    user=user,
                    CardDetails = authorization_email,
                    last4digits=last4digits,
                    authorization_email=authorization_email,
                    expiry_month=expiry_month,
                    expiry_year=expiry_year,
                    authorization_code=authorization_code,
                    card_type=card_type,
                    card_bank=bank,
                    is_active=True if reuseable else False,
                )
                card.save()
                return {"status": True, "message": "Card has been added"}
            except (IntegrityError or IndexError) as errror:
                return {
                    "status": False,
                    "error": "DUPLICATE_CARD",
                    "message": "Could not add card, Already Exist",
                }
        else:
            return {
                "status": False,
                "error": "VERIFICATION_ERROR",
                "message": verify_response["message"],
            }
