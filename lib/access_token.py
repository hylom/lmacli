"""LINE Message API: get channel access token v2.1"""

import json

from .interface import Interface

class TokenInterface(Interface):
    def set_parser(self, name, subparsers):
        '''add ArgumentParser to subparsers'''
        token = subparsers.add_parser(name)
        token_subparsers = token.add_subparsers(dest='subcommand')
        token_create = token_subparsers.add_parser('create')
        token_list = token_subparsers.add_parser('list')
        token_list.add_argument('--token',
                                action='store_true',
                                help="get tokens instead of key id")
        token_verify = token_subparsers.add_parser('verify')
        token_verify.add_argument('token',
                                  help="access token")
        token_revoke = token_subparsers.add_parser('revoke')
        token_revoke.add_argument('token',
                                  help="access token")

    def execute(self, args):
        if args.subcommand == "list":
            if args.token:
                resp = self.list_tokens()
            else:
                resp = self.list()
            print(resp)
            return
        elif args.subcommand == "create":
            resp = self.create()
            print(resp)
            return
        elif args.subcommand == "verify":
            resp = self.verify(args.token)
            print(resp)
            return
        elif args.subcommand == "revoke":
            resp = self.revoke(args.token)
            print(resp)
            return
        else:
            print("invalid subcommand")
    
    def create(self):
        path = "/oauth2/v2.1/token"
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
        return self.post_request(path, data, headers)

    def list(self):
        jwt = self.create_jwt()
        data = {
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": jwt,
        }
        path = "/oauth2/v2.1/tokens/kid?" + parse.urlencode(data)
        return self.get_request(path)

    def list_tokens(self):
        jwt = self.create_jwt()
        data = {
            "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer",
            "client_assertion": jwt,
        }
        path = "/oauth2/v2.1/tokens?" + parse.urlencode(data)
        return self.get_request(path)

    def verify(self, token):
        path = "/oauth2/v2.1/verify?access_token=" + token
        return self.get_request(path)

    def revoke(self, token):
        config = self.get_config()
        data = {
            "client_id": config["ChannelId"],
            "client_secret": config["ChannelSecret"],
            "access_token": token,
        }
        path = "/oauth2/v2.1/revoke"
        return self.post_request(path, data, headers)
