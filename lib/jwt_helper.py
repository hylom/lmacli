"""JWT Helper"""

import json
import time
from jose import jwt

def create_jwt(config, payload={}):
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
