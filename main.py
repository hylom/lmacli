#!/usr/bin/env python3

import argparse
import configparser
import lib.access_token
import lib.user

def main():
    parser = argparse.ArgumentParser(description='LINE Message API CLI.')

    # `token' commands
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

    # `user' commands
    user = subparsers.add_parser('user')
    token_subparsers = user.add_subparsers(dest="subcommand")
    user_profile = token_subparsers.add_parser('profile')
    user_profile.add_argument('user_id',
                              help="user ID")

    # do parsing
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    default_cfg = cfg["default"]

    if args.command == "token":
        if args.subcommand == "list":
            if args.token:
                resp = lib.access_token.list_tokens(default_cfg)
            else:
                resp = lib.access_token.list(default_cfg)
            print(resp)
            return
        elif args.subcommand == "create":
            resp = lib.access_token.create(default_cfg)
            print(resp)
            return
        elif args.subcommand == "list":
            resp = lib.access_token.list(default_cfg)
            print(resp)
            return
        elif args.subcommand == "revoke":
            resp = lib.access_token.revoke(default_cfg, args.token)
            print(resp)
            return
    elif args.command == "user":
        if args.subcommand == "profile":
            resp = lib.user.get_profile(default_cfg, args.user_id)
            print(resp)
            return
            

if __name__ == '__main__':
    main()
