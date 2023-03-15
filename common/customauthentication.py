from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        # try:
        #     # ... original code to authenticate the token ...
        # except exceptions.AuthenticationFailed as e:
        #     raise AuthenticationFailed({
        #         'detail': 'Token is expired',
        #         'detail':{},
        #         'status':False
        #     })
        pass
