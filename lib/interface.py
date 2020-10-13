"""interface base class"""

from urllib.error import HTTPError
from urllib import request, parse, error

from linebot import LineBotApi
import json
import time
from jose import jwt

class Interface():
    def __init__(self, config):
        self._config = config

    def get_config(self):
        return self._config

    def get_endpoint(self, path):
        try:
            env = self.get_config()['Environment'].lower()
        except KeyError:
            env = 'real'

        if env == 'beta':
            return 'https://api.line-beta.me{}'.format(path)
        return 'https://api.line.me{}'.format(path)

    def get_request(self, path, headers={}):
        try:
            resp = request.urlopen(self.get_endpoint(path))
        except HTTPError as e:
            if (e.code == 400):
                return json.loads(e.read().decode('utf-8'))
            return {}

        return json.loads(resp.read().decode('utf-8'))

    def post_request(self, path, data=None, json=None, headers={}):
        if data:
            data = parse.urlencode(data).encode("ascii")
        if json:
            pass
            
        req = request.Request(self.get_endpoint(path),
                              data=data,
                              headers=headers,
                              method="POST")

        try:
            resp = request.urlopen(req)
        except HTTPError as e:
            if e.code == 400:
                return json.loads(e.read().decode('utf-8'))
            return {}
        return json.loads(resp.read().decode('utf-8'))

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
