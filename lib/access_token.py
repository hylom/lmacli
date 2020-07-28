"""LINE Message API: get channel access token v2.1"""

from urllib import request, parse, error
from urllib.error import HTTPError
import json

from .interface import Interface

class TokenInterface(Interface):
    def create(self):
        API_URL = "https://api.line.me/oauth2/v2.1/token"
        payload = {
            "token_exp": 60 * 60 * 24 * 30, # 60 sec * 60 min * 24 hour * 30 day
        }
        jwt = self.create_jwt(payload);
        data = {
            "grant_type": "client_credentials",
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": jwt,
        }
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
    
        req = request.Request(API_URL,
                              data=parse.urlencode(data).encode("ascii"),
                              headers=headers,
                              method="POST")
        try:
            resp = request.urlopen(req)
        except HTTPError as e:
            if (e.code == 400):
                return json.loads(e.read().decode('utf-8'))
            return {}

        return json.loads(resp.read().decode('utf-8'))

    def list(self):
        API_URL = "https://api.line.me/oauth2/v2.1/tokens/kid"
        jwt = self.create_jwt()
        data = {
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": jwt,
        }

        url = API_URL + "?" + parse.urlencode(data)
        try:
            resp = request.urlopen(url)
        except HTTPError as e:
            if (e.code == 400):
                return json.loads(e.read().decode('utf-8'))
            return {}

        return json.loads(resp.read().decode('utf-8'))

    def list_tokens(self):
        API_URL = "https://api.line.me/oauth2/v2.1/tokens"
        jwt = self.create_jwt()
        data = {
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": jwt,
        }

        url = API_URL + "?" + parse.urlencode(data)
        try:
            resp = request.urlopen(url)
        except HTTPError as e:
            if (e.code == 400):
                return json.loads(e.read().decode('utf-8'))
            return {}

        return json.loads(resp.read().decode('utf-8'))

    def revoke(self, token):
        config = self.get_config()
        API_URL = "https://api.line.me/oauth2/v2.1/revoke"
        data = {
            "client_id": config["ChannelId"],
            "client_secret": config["ChannelSecret"],
            "access_token": token,
        }
        req = request.Request(API_URL,
                              data=parse.urlencode(data).encode("ascii"),
                              headers={},
                              method="POST")
        try:
            resp = request.urlopen(req)
        except HTTPError as e:
            if (e.code == 400):
                return json.loads(e.read().decode('utf-8'))
            return e

        return
