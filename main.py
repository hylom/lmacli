#!/usr/bin/env python3

import argparse
import configparser
import lib.access_token as access_token

def main():
    parser = argparse.ArgumentParser(description='LINE Message API CLI.')

    subparsers = parser.add_subparsers(dest="command")
    token = subparsers.add_parser('token')

    token_subparsers = token.add_subparsers(dest="subcommand")
    token_create = token_subparsers.add_parser('create')
    token_list = token_subparsers.add_parser('list')
    token_list.add_argument('--token',
                            const=True,
                            action='store_const',
                            help="get tokens instead of key id")
    token_revoke = token_subparsers.add_parser('revoke')
    token_revoke.add_argument('token',
                              help="access token")

    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    default_cfg = cfg["default"]

    if args.command == "token":
        if args.subcommand == "list":
            if args.token:
                resp = access_token.list_tokens(default_cfg)
            else:
                resp = access_token.list(default_cfg)
            print(resp)
            return
        elif args.subcommand == "create":
            resp = access_token.create(default_cfg)
            print(resp)
            return
        elif args.subcommand == "list":
            resp = access_token.list(default_cfg)
            print(resp)
            return
        elif args.subcommand == "revoke":
            print(args.token)
            resp = access_token.revoke(default_cfg, args.token)
            print(resp)
            return

if __name__ == '__main__':
    main()
