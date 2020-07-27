"""LINE Message API: user related API"""

from urllib import request, parse, error
from urllib.error import HTTPError
import json

def get_profile(config, user_id):
    API_URL = 'https://api.line.me/v2/bot/profile/'
    headers = { 'Authorization': 'Bearer ' + config["ChannelAccessToken"] }

    req = request.Request(API_URL + user_id,
                          headers=headers,
                          method="GET")

    try:
        resp = request.urlopen(req)
    except HTTPError as e:
        if (e.code == 400):
            return json.loads(e.read().decode('utf-8'))
        return {}

    return json.loads(resp.read().decode('utf-8'))

