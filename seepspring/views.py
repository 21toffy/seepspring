from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from accounts.models import CustomUser, BvnData, BankAccountDetails
from banks.models import NigerianBanks
from loan.models import LoanLevel, LoanPurpose, Interest
from django.db import transaction
from common.load import get_users, get_loan_level, get_loan_purpose, get_loan_interest




@api_view(('GET',))
def home_page(request):
    users = CustomUser.objects.all()
    return Response({"details":"Hello World!, I think the DB was set up properly"})



@api_view(('GET',))
def populate_banks(request):
    bank_codes = {
  "Access Bank": "044",
  "Access Bank (Diamond)": "063",
  "ALAT by WEMA": "035A",
  "ASO Savings and Loans": "401",
  "Bowen Microfinance Bank": "50931",
  "CEMCS Microfinance Bank": "50823",
  "Citibank Nigeria": "023",
  "Ecobank Nigeria": "050",
  "Ekondo Microfinance Bank": "562",
  "Eyowo": "50126",
  "Fidelity Bank": "070",
  "First Bank of Nigeria": "011",
  "First City Monument Bank": "214",
  "FSDH Merchant Bank Limited": "501",
  "Globus Bank": "00103",
  "Guaranty Trust Bank": "058",
  "Hackman Microfinance Bank": "51251",
  "Hasal Microfinance Bank": "50383",
  "Heritage Bank": "030",
  "Ibile Microfinance Bank": "51244",
  "Jaiz Bank": "301",
  "Keystone Bank": "082",
  "Kuda Bank": "50211",
  "Lagos Building Investment Company Plc.": "90052",
  "One Finance": "565",
  "Parallex Bank": "526",
  "Parkway - ReadyCash": "311",
  "Polaris Bank": "076",
  "Providus Bank": "101",
  "Rubies MFB": "125",
  "Sparkle Microfinance Bank": "51310",
  "Stanbic IBTC Bank": "221",
  "Standard Chartered Bank": "068",
  "Sterling Bank": "232",
  "Suntrust Bank": "100",
  "TAJ Bank": "302",
  "TCF MFB": "51211",
  "Titan Bank": "102",
  "Union Bank of Nigeria": "032",
  "United Bank For Africa": "033",
  "Unity Bank": "215",
  "VFD": "566",
  "Wema Bank": "035",
  "Zenith Bank": "057"
}
    with transaction.atomic():
        try:
            for bank, code in bank_codes.items():
                NigerianBanks.objects.create(
                    bank_name = bank,
                    bank_code = code
                )
        except Exception as ex:
            return Response({"details":str(ex)}, 400)
        return Response({"details":"banks populated fully"}, 200)



import json
@api_view(('GET',))
def populate_user(request):
    data = get_users()
    loan_level = get_loan_level()
    loan_purpose = get_loan_purpose()
    loan_interest = get_loan_interest()


    count: int = 0
    loanlevel_count: int = 0
    loan_interest_count : int = 0
    loanpurpose_count: int = 0

    all_purpose = LoanPurpose.objects.all()
    for i in all_purpose:
        i.delete()
    all_interest = Interest.objects.all()
    for i in all_interest:
        i.delete()

    for item in loan_level:
        LoanLevel.objects.create(
            level = item["level"],
            loan_name = item["loan_name"],
            max_amount = item["max_amount"],
            min_amount = item["min_amount"],
            cycle = item["cycle"],
            days_tenure = item["days_tenure"],
        )
        loanlevel_count += 1


    for item in loan_purpose:
        LoanPurpose.objects.create(
            id = item["id"],
            purpose = item["purpose"],
            active = True
        )
        loanpurpose_count += 1

    for item in loan_interest:
        Interest.objects.create(
            id = item["id"],
            interest_name = item["interest_name"],
            active = True
        )
        loan_interest_count += 1

    for item in data:
        print(item['email'])        
        user = CustomUser.objects.filter(phone_number=item['phone_number'] )

        # print(user.is_staff(), 5454)
        if not user.exists():
            user_obj = CustomUser.objects.create(
                email=item['email'],
                phone_number = item['phone_number'],
                password = item['password'],
                bvn_phone_number = item['bvn_phone_number'],                
                bvn_address = item['bvn_address'],
                state_of_origin = item['state_of_origin'],                
                state_of_residence = item['state_of_residence'],
                lga_of_origin = item['lga_of_origin'],                
                first_name = item['first_name'],
                last_name = item['last_name'],                
                middle_name = item['middle_name'],
                gender = item['gender'],                
                dob = item['dob'],
                lga_of_residence = item['lga_of_residence'],                
                marital_status = item['marital_status'],
                nationality = item['nationality'],                
                bvn = item['bvn'],
                is_staff = True,
                is_active = True
                )
            count +=1


            BankAccountDetails.objects.create(
                    user = user_obj,
                    # id = "798b4a3e-c8c4-4dfb-9773-f40bab372618",
                    bank_name = "GT Bank",
                    account_number = "08178765432",
                    account_name = "tofunmi okedeji",
                )


            BvnData.objects.get_or_create(
                user = user_obj,
                bvn = item["bvn_data"]['bvn'],               
                first_name = item["bvn_data"]['first_name'],               
                last_name = item["bvn_data"]['last_name'],               
                middle_name = item["bvn_data"]['middle_name'],               
                gender = item["bvn_data"]['gender'],               
                date_of_birth = item["bvn_data"]['date_of_birth'],               
                phone_number1 = item["bvn_data"]['phone_number1'],               
                level_of_account = item["bvn_data"]['level_of_account'],               
                image = item["bvn_data"]['image'],               
                lga_of_origin = item["bvn_data"]['lga_of_origin'],               
                lga_of_residence = item["bvn_data"]['lga_of_residence'],               
                marital_status = item["bvn_data"]['marital_status'],               
                name_on_card = item["bvn_data"]['name_on_card'],               
                nationality = item["bvn_data"]['nationality'],               
                nin = item["bvn_data"]['nin'],               
                phone_number2 = item["bvn_data"]['phone_number2'],               
                reference = item["bvn_data"]['reference'],               
                registration_date = item["bvn_data"]['registration_date'],               
                residential_address = item["bvn_data"]['residential_address'],               
                state_of_origin = item["bvn_data"]['state_of_origin'],               
                state_of_residence = item["bvn_data"]['state_of_residence'],               
                title = item["bvn_data"]['title'],               
                watch_listed = item["bvn_data"]['watch_listed'],)
            
    return Response({"status":"run succesfully", "count":count, "loanlevel_count":loanlevel_count, 'loanpurpose_count':loanpurpose_count,"loan_interest_count":loan_interest_count})



        













