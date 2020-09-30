"""LINE Message API: get channel access token v2.0"""

from urllib import request, parse, error
from urllib.error import HTTPError
import json

from .interface import Interface

class Token20Interface(Interface):
    def create(self):
        API_URL = "https://api.line.me/v2/oauth/accessToken"
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        config = self.get_config()
        data = {
            "grant_type": "client_credentials",
            "client_id": config['ChannelId'],
            "client_secret": config['ChannelSecret'],
        }
    
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

    def revoke(self, token):
        config = self.get_config()
        API_URL = "https://api.line.me/v2/oauth/revoke"
        headers = { "Content-Type": "application/x-www-form-urlencoded" }
        data = {
            "access_token": token,
        }
        req = request.Request(API_URL,
                              data=parse.urlencode(data).encode("ascii"),
                              headers=headers,
                              method="POST")
        try:
            resp = request.urlopen(req)
        except HTTPError as e:
            if (e.code == 400):
                return json.loads(e.read().decode('utf-8'))
            return e
        return
