"""interface base class"""

from linebot import LineBotApi
import json
import time
from jose import jwt

class Interface():
    def __init__(self, config):
        self._config = config

    def get_config(self):
        return self._config

    def get_api_client(self):
        token = self.get_config()['ChannelAccessToken']
        return LineBotApi(token)
    
    def create_jwt(self, payload={}):
        config = self.get_config()
        with open(config["AssertionKeyFile"], "r") as f:
            assertion_key = json.load(f)

        header = {
            "alg": "RS256",
            "typ": "JWT",
            "kid": assertion_key["kid"],
        }
    
        _payload = {
            "iss": config["ChannelId"],
            "sub": config["ChannelId"],
            "aud": "https://api.line.me/",
            "exp": int(time.time()) + 60 * 30,
        }
        _payload.update(payload)

        return jwt.encode(_payload,
                          assertion_key,
                          algorithm='RS256',
                          headers=header)
