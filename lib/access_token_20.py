"""LINE Message API: get channel access token v2.0"""

from urllib import request, parse, error
from urllib.error import HTTPError
import json

from .interface import Interface

class Token20Interface(Interface):
    def set_parser(self, name, subparsers):
        token = subparsers.add_parser(name)
        token_subparsers = token.add_subparsers(dest='subcommand')
        token_create = token_subparsers.add_parser('create')
        token_verify = token_subparsers.add_parser('verify')
        token_verify.add_argument('token',
                                  help="access token")
        token_revoke = token_subparsers.add_parser('revoke')
        token_revoke.add_argument('token',
                                  help="access token")

    def execute(self, args):
        if args.subcommand == "create":
            resp = self.create()
            print(resp)
            return
        elif args.subcommand == "revoke":
            resp = self.revoke(args.token)
            print(resp)
            return

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
