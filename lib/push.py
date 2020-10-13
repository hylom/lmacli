"""LINE Message API: push related API"""

from linebot.models import AudienceRecipient, Filter, Limit
import json
import argparse

from .interface import Interface
from lib.shim import TextSendMessage

class PushInterface(Interface):
    def set_parser(self, name, subparsers):
        push = subparsers.add_parser(name)
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
        push_msg.add_argument('-m', '--message',
                              type=argparse.FileType('r'),
                              action='append',
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

    def execute(self, args):
        msgs = []
        if args.text:
            msgs = [linebot.models.TextSendMessage(text=t) for t in args.text]
        if args.message:
            msgs += self._create_message_object([json.load(fp) for fp in args.message])
            [fp.close() for fp in args.message]
        if args.subcommand == "message":
            self.message(args.to, msgs)
            return
        elif args.subcommand == 'multicast':
            self.multicast(args.to, msgs)
            return
        elif args.subcommand == 'narrowcast':
            self.narrowcast(args.to, msgs)
            return
        elif args.subcommand == 'broadcast':
            self.broadcast(args.text, msgs)
            return

    def _create_message_object(messages=[]):
        result = []
        for msg in messages:
            m = None
            if msg["type"] == "flex":
                m = linebot.models.FlexSendMessage(alt_text=msg["altText"],
                                                   contents=msg["contents"])
            if msg["type"] == "location":
                m = linebot.models.LocationSendMessage.new_from_json_dict(msg)
            if msg["type"] == "sticker":
                m = linebot.models.StickerSendMessage.new_from_json_dict(msg)
            if msg["type"] == "image":
                m = linebot.models.ImageSendMessage.new_from_json_dict(msg)
            if msg["type"] == "template":
                m = linebot.models.TemplateSendMessage.new_from_json_dict(msg)
            if msg["type"] == "text":
                m = TextSendMessage.new_from_json_dict(msg)
                print(m)

            if m:
                result.append(m)
        return result

    def message(self, recipient, messages=[]):
        api = self.get_api_client()
        api.push_message(recipient, messages)

    def multicast(self, recipients, messages=[]):
        api = self.get_api_client()
        api.multicast(recipients, messages)
        
    def narrowcast(self, group_id, texts=[], messages=[],
                   filter_demographic=None, limit_max=None,
                   notification_disabled=False):
        api = self.get_api_client()
        recipient = AudienceRecipient(group_id=group_id)
        api.narrowcast(messages, recipient, Filter(), Limit())

    def broadcast(self, texts=[], messages=[]):
        api = self.get_api_client()
        api.broadcast(messages)
        
