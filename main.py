#!/usr/bin/env python3

import argparse
import configparser
import json

from linebot.models import FlexSendMessage, TextSendMessage

from lib.access_token import TokenInterface
from lib.user import UserInterface
from lib.push import PushInterface
from lib.audience import AudienceInterface
from lib.insight import InsightInterface

def main():
    parser = argparse.ArgumentParser(description='LINE Message API CLI.')
    subparsers = parser.add_subparsers(dest="command", required=True)

    # `token' commands
    token = subparsers.add_parser('token')
    token_subparsers = token.add_subparsers(dest='subcommand')
    token_create = token_subparsers.add_parser('create')
    token_list = token_subparsers.add_parser('list')
    token_list.add_argument('--token',
                            action='store_true',
                            help="get tokens instead of key id")
    token_revoke = token_subparsers.add_parser('revoke')
    token_revoke.add_argument('token',
                              help="access token")

    # `user' commands
    user = subparsers.add_parser('user')
    user.add_argument('--hoge', help="hogehoge")
    user_subparsers = user.add_subparsers(dest='subcommand')
    user_profile = user_subparsers.add_parser('profile')
    user_profile.add_argument('user_id',
                              help="user ID")

    # 'push` commands
    push = subparsers.add_parser('push')
    push.add_argument('-m', '--message', nargs='*',
                      type=argparse.FileType('r'),
                      help="message json file to send")
    push.add_argument('-t', '--text',
                          action='append',
                          help='text to send')
    push_subparsers = push.add_subparsers(dest='subcommand')
    push_msg = push_subparsers.add_parser('message')
    push_msg.add_argument('to',
                          help='ID to send message')
    push_msg.add_argument('-t', '--text',
                          action='append',
                          help='text to send')
    push_msg.add_argument('-m', '--message', nargs='*',
                          type=argparse.FileType('r'),
                          help="message json file to send")
    push_multi = push_subparsers.add_parser('multicast')
    push_multi.add_argument('to',
                            nargs='+',
                            help='IDs to send message')
    push_multi.add_argument('-t', '--text',
                            action='append',
                            help='text to send')
    push_multi.add_argument('-m', '--message', nargs='*',
                            type=argparse.FileType('r'),
                            help="message json file to send")
    push_narrow = push_subparsers.add_parser('narrowcast')
    push_narrow.add_argument('to',
                             help='group ID to send message')
    push_narrow.add_argument('-t', '--text',
                             action='append',
                             help='text to send')
    push_narrow.add_argument('-m', '--message', nargs='*',
                             type=argparse.FileType('r'),
                             help="message json file to send")
    push_broad = push_subparsers.add_parser('broadcast')
    push_broad.add_argument('-t', '--text',
                            action='append',
                            help='text to send')
    push_broad.add_argument('-m', '--message', nargs='*',
                            type=argparse.FileType('r'),
                            help="message json file to send")

    # `insight' commands
    insight = subparsers.add_parser('insight')
    insight_subp = insight.add_subparsers(dest='subcommand')
    insight_followers = insight_subp.add_parser('followers')
    insight_followers.add_argument('date',
                                   help='date (yyyyMMdd)')
    insight_delivery = insight_subp.add_parser('delivery')
    insight_delivery.add_argument('date',
                                  help='date (yyyyMMdd)')
    
    # `audience' commands
    aud = subparsers.add_parser('audience')
    aud_subparsers = aud.add_subparsers(dest='subcommand')
    aud_list = aud_subparsers.add_parser('list')

    # do parsing
    args = parser.parse_args()
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    default_cfg = cfg["default"]

    if args.command == "token":
        token = TokenInterface(default_cfg)
        if args.subcommand == "list":
            if args.token:
                resp = token.list_tokens()
            else:
                resp = token.list()
            print(resp)
            return
        elif args.subcommand == "create":
            resp = token.create()
            print(resp)
            return
        elif args.subcommand == "revoke":
            resp = token.revoke(args.token)
            print(resp)
            return
    elif args.command == "user":
        user = UserInterface(default_cfg)
        if args.subcommand == "profile":
            resp = user.get_profile(args.user_id)
            print(resp)
            return
    elif args.command == "push":
        push = PushInterface(default_cfg)
        msgs = []
        if args.text:
            msgs = [TextSendMessage(text=t) for t in args.text]
        msgs += _create_message_object([json.load(fp) for fp in args.message])
        if args.subcommand == "message":
            push.message(args.to, msgs)
            return
        elif args.subcommand == 'multicast':
            push.multicast(args.to, msgs)
            return
        elif args.subcommand == 'narrowcast':
            push.narrowcast(args.to, msgs)
            return
        elif args.subcommand == 'broadcast':
            push.broadcast(args.text, msgs)
            return
    elif args.command == "audience":
        aud = AudienceInterface(default_cfg)
        if args.subcommand == "list":
            resp = aud.list()
            print(resp)
            return
    elif args.command == "insight":
        insight = InsightInterface(default_cfg)
        if args.subcommand == "followers":
            resp = insight.followers(args.date)
            print(resp)
            return
        if args.subcommand == "delivery":
            resp = insight.delivery(args.date)
            print(resp)
            return

def _create_message_object(messages=[]):
    result = []
    for msg in messages:
        if msg["type"] == "flex":
            m = FlexSendMessage(alt_text=msg["altText"],
                                contents=msg["contents"])
            result.append(m)
    return result

if __name__ == '__main__':
    main()
