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
def custom_serializer_error(error) -> str:
    for i in error:
        error_message = i +" " + error[i][0][4:]
    return error_message

def custom_user_serializer_error(error) -> str:
    for i in error:
        error_message = i +" " + error[i][0]
    return error_message

def generate_four_random_digits() -> int:
    import random
    number = random.randint(1111,9999)
    return number
    

def get_first_serializer_error(errors) -> str:
    # function to get the first error message from a serializer's errors
    for i in errors:
        # Extract the error message
        error_message = i + errors[i][0][4:]
    return error_message


import datetime
def get_date_yyyy_mm_dd():
    today = datetime.date.today()
    return today.strftime('%Y-%m-%d')


def getdate_time_yyyy_mm_dd_hh_ss_sm():
    from datetime import datetime
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return current_datetime


def convert__to_datetime():
    from datetime import datetime, date

    datetime_string = getdate_time_yyyy_mm_dd_hh_ss_sm()
    datetime_object = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")
    date_object = datetime_object.date()
    return date_object
def get_current_month():
    import datetime
    current_month = datetime.datetime.now().strftime("%B")
    return current_month


def get_current_month_as_string():
    current_month_number = datetime.datetime.now().month
    return current_month_number


import random  
import string  
def unique_string(length :int) -> str:  
    letters = string.ascii_lowercase # define the specific string  
    result = ''.join((random.sample(letters, length)))   
    return result

def unique_id() -> int:  
    from random import randint
    id = str(randint(1001, 99000))
    return id



def get_international_number(number: str) -> str:  
    remove_zero = number[1:]
    return "234" + remove_zero

