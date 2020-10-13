"""LINE Message API: user related API"""

from urllib import request, parse, error
from urllib.error import HTTPError
import json

from .interface import Interface

class UserInterface(Interface):
    def set_parser(self, name, subparsers):
        user = subparsers.add_parser(name)
        user.add_argument('--hoge', help="hogehoge")
        user_subparsers = user.add_subparsers(dest='subcommand')
        user_profile = user_subparsers.add_parser('profile')
        user_profile.add_argument('user_id',
                                  help="user ID")

    def execute(self, args):
        if args.subcommand == "profile":
            resp = self.get_profile(args.user_id)
            print(resp)
            return

    def get_profile(self, user_id):
        config = self.get_config()
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

