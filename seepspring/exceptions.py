from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler

class CustomTokenException(APIException):
    status_code = 401
    default_detail = 'Given token not valid for any token type'
    default_code = 'token_not_valid'
    status = False
    # detail = "Token expired"



def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data['status'] = False
    
    return response
