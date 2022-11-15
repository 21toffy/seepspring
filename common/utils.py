from datetime import datetime
import pyotp
from rest_framework.response import Response
import base64
from decimal import *
from seepspring.settings import (SECRET_KEY, OTP_EXPIRY_TIME)

import json
import pathlib
import requests

def float_to_decimal(f):
    "Convert a floating point number to a Decimal with no loss of information"
    n, d = f.as_integer_ratio()
    numerator, denominator = Decimal(n), Decimal(d)
    ctx = Context(prec=60)
    result = ctx.divide(numerator, denominator)
    while ctx.flags[Inexact]:
        ctx.flags[Inexact] = False
        ctx.prec *= 2
        result = ctx.divide(numerator, denominator)
    return result



def todays_date():
    import datetime
    todays_date = datetime.date.today()
    return todays_date


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + SECRET_KEY


def generate_token(phone):
    try:
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.TOTP(key,interval = OTP_EXPIRY_TIME)  # TOTP Model for OTP is created
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return OTP.now()  # Just for demonstration

    except Exception as e:
        return 12345
def custom_serializer_error(error):
    errors = error
    string = (str(errors))
    respo = string.split(":")[1].split("=")[1].split(",")[0].split("'")[1]
    return respo


def generate_four_random_digits() -> int:
    import random
    number = random.randint(1111,9999)
    return number
    

# def openconfig() -> dict:
#     with open("config.json", "r") as f:
#         config = json.load(f)
#         return config

