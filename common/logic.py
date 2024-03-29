import json
import pathlib
import requests
from seepspring.settings import (
    SENDCHAMP_AUTHORIZATION,
    SENDCHAMP_SENDER_ID,
    SENDCHAMP_URL
)




class GetBVN(object):
    def __init__(self, bvn_number: str):
        self.url = self.openconfig()["dojah"]["url"]
        self.app_id = self.openconfig()["dojah"]["app_id"]
        self.bvn_number =  bvn_number

        
    def openconfig(self) -> dict:
        with open("config.json", "r") as f:
            config = json.load(f)
            return config


    def build_url(self) -> str:
        url = f"{self.url}?bvn={self.bvn_number}?AppId={self.app_id}"
        return url

    def get_headers(self) -> dict:
        headers = {"accept": "text/plain", "Authorization":self.get_apikey()}
        return headers

    def get_apikey(self) -> str:
        config = self.openconfig()
        api_key = config["dojah"]["api_key"]
        return api_key

    def get_app_id(self) -> str:
        config = self.openconfig()
        app_id = config["dojah"]["app_id"]
        return app_id

    def request_bvn(self):
        try:
            response = requests.get(self. build_url(), headers=self.get_headers())
            return response
        except Exception as e:
            return  e

import logging

logger = logging.getLogger(__name__)
logger = logging.getLogger('sendchamp_logs')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('sendchamp_logs.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class SendSMS:
    def __init__(self, payload: dict) -> None:
        # self.url = self.openconfig()["sendchamp"]["url"]
        self.url = SENDCHAMP_URL

        self.payload = payload
        # self.sender_id = self.openconfig()["sendchamp"]["sender_id"]
        self.sender_id = SENDCHAMP_SENDER_ID

    def build_sms(self):
        payload = self.payload
        return {
            "to": payload['to'],
            "message": payload["message"],
            "sender_name": payload["sender_name"],
            "route": payload["route"]
        } 


    def get_authorization(self) -> str:
        # config = self.openconfig()
        # authorization = config["sendchamp"]["authorization"]
        authorization = SENDCHAMP_AUTHORIZATION
        return "sendchamp_live_$2a$10$EMqyCE4.Hd/gzgbXLPY6PuTAs8QkQQTt0aDkXouyYJaBDQiKdy0Lu"
        # return authorization

    # def openconfig(self) -> dict:
    #     with open("config.json", "r") as f:
    #         config = json.load(f)
    #         return config

    def get_headers(self) -> dict:
        headers = {"accept": "application/json","content-type": "application/json", "Authorization":"Bearer " + self.get_authorization()}
        return headers

    
    def send_otp(self) ->dict:
        try:

            response = requests.post(self.url, json=self.payload, headers=self.get_headers())
            # print("url", self.url)
            # print("payload", self.payload)
            # print("headers", self.get_headers())
            # print("response", response.json())
            logger.debug(f"URL: {str(self.url)}")
            logger.debug(f"payload: {str(self.payload)}")
            logger.debug(f"headers: {str(self.get_headers())}")
            logger.debug(f"response: {str(response.json())}")


            return response.json()
        except Exception as e:
            print(str(e))
            return  {
                    "data": None,
                    "message": f"Something went wrong {str(e)}",
                    "status": 400,
                    "code": 400
                    }
            






