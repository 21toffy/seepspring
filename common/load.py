def get_users():
    return [
    {
        "email": "oketofokea@gmail.com",
        "phone_number": "08104756718",
        "password": "pbkdf2_sha256$260000$aEHo64g8ehS6I1mPUbenxj$Xw+g3BxEwN9OLfMyTEYB9zu0XVSKA/kuDF+5tgDRyak=",
        "bvn_phone_number": "08104756718",
        "bvn_address": "married",
        "state_of_origin": "23 jesus street",
        "state_of_residence": "3",
        "lga_of_origin": "https://www.ufebfuebfu.ybf",
        "first_name": "tofunmi",
        "last_name": "okedeji",
        "middle_name": "babajuwon",
        "gender": "Male",
        "dob": "1997-08-06",
        "lga_of_residence": "married",
        "marital_status": "23 jesus street",
        "nationality": "3",
        "bvn": "22213123999",
        "bvn_data": {
            "bvn": "22350348240",
            "first_name": "ADEOLA",
            "last_name": "AYO",
            "middle_name": "MICHEAL",
            "gender": "Male",
            "date_of_birth": "1972-02-19",
            "phone_number1": "08099434292",
            "image": "/9j/3AAQSkZJGgABAgBBBQABAAD/",
            "last_name": "AYO",
            "level_of_account": "Level 2 - Medium Level Accounts",
            "lga_of_origin": "Odo Otin",
            "lga_of_residence": "Ilorin South",
            "marital_status": "Single",
            "middle_name": "OLUWATIMILEYIN",
            "name_on_card": "MICHEAL, ADEOLA A",
            "nationality": "Nigeria",
            "nin": "",
            "phone_number1": "08099434292",
            "phone_number2": "",
            "reference": "91b126d1-2467-42fc-b8d5-1cbd32257954",
            "registration_date": "21-Mar-2018",
            "residential_address": "24, ADELABU OWODE, ILORIN",
            "state_of_origin": "Osun State",
            "state_of_residence": "Kwara State",
            "title": "Mr",
            "watch_listed": "NO"
        }
    },
    {
        "email": "olaitanokedeji@gmail.com",
        "phone_number": "08023178165",
        "password": "pbkdf2_sha256$260000$aEHo64g8ehS6I1mPUbenxj$Xw+g3BxEwN9OLfMyTEYB9zu0XVSKA/kuDF+5tgDRyak=",
        "bvn_phone_number": "08023178165",
        "bvn_address": "married",
        "state_of_origin": "23 jesus street",
        "state_of_residence": "3",
        "lga_of_origin": "https://www.ufebfuebfu.ybf",
        "first_name": "olaitan",
        "last_name": "okedeji",
        "middle_name": "alaba",
        "gender": "Male",
        "dob": "1997-08-06",
        "lga_of_residence": "married",
        "marital_status": "23 jesus street",
        "nationality": "3",
        "bvn": "22213123999",
        "bvn_data": {
            "bvn": "22350348240",
            "first_name": "ADEOLA",
            "last_name": "AYO",
            "middle_name": "MICHEAL",
            "gender": "Male",
            "date_of_birth": "1972-02-19",
            "phone_number1": "08099434292",
            "image": "/9j/3AAQSkZJGgABAgBBBQABAAD/",
            "last_name": "AYO",
            "level_of_account": "Level 2 - Medium Level Accounts",
            "lga_of_origin": "Odo Otin",
            "lga_of_residence": "Ilorin South",
            "marital_status": "Single",
            "middle_name": "OLUWATIMILEYIN",
            "name_on_card": "MICHEAL, ADEOLA A",
            "nationality": "Nigeria",
            "nin": "",
            "phone_number1": "08099434292",
            "phone_number2": "",
            "reference": "91b126d1-2467-42fc-b8d5-1cbd32257954",
            "registration_date": "21-Mar-2018",
            "residential_address": "24, ADELABU OWODE, ILORIN",
            "state_of_origin": "Osun State",
            "state_of_residence": "Kwara State",
            "title": "Mr",
            "watch_listed": "NO"
        }
    }
]

def get_loan_level():
    return [
        {
            "level": 1,
            "loan_name":"level 1",
            "max_amount" :5000,
            "min_amount":1000,
            "cycle":2,
            "days_tenure": 7,
        },
                {
            "level": 2,
            "loan_name":"level 2",
            "max_amount" :15000,
            "min_amount":1000,
            "cycle":2,
            "days_tenure": 14,
        },
                {
            "level": 1,
            "loan_name":"level 3",
            "max_amount" :50000,
            "min_amount":1000,
            "cycle":2,
            "days_tenure": 14,
        }
    ]

def get_loan_purpose():
    return  [
        {
            "id": "f3884557-83b5-45c1-93cb-cc0fcce33d4e",
            "purpose":"daily consumption",
            "active":True
        },
                {
            "id": "f3884557-83b5-45c1-93cb-cc0fcce33d5e",
            "purpose":"medical bills",
            "active":True
        },
            {
            "id": "f3884557-83b5-45c1-93cb-cc0fcce33d6e",
            "purpose":"School fees",
            "active":True
        }
        
    ]



def get_loan_interest():
    return  [
        {
            "id": "493895df-c772-4218-a211-4f55e9c3be02",
            "interest_name":"basic interest",
            "active":True
        },
                {
            "id": "f3884557-83b5-45c1-93cb-cc0fcce33d5e",
            "interest_name":"Christmas Interest",
            "active":False
        }
        
    ]