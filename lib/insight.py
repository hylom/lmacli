"""LINE Message API: insight related API"""

import json

from .interface import Interface

class InsightInterface(Interface):
    def set_parser(self, name, subparsers):
        insight = subparsers.add_parser(name)
        insight_subp = insight.add_subparsers(dest='subcommand')
        insight_followers = insight_subp.add_parser('followers')
        insight_followers.add_argument('date',
                                       help='date (yyyyMMdd)')
        insight_delivery = insight_subp.add_parser('delivery')
        insight_delivery.add_argument('date',
                                      help='date (yyyyMMdd)')

    def execute(self, args):
        if args.subcommand == "followers":
            resp = self.followers(args.date)
            print(resp)
            return
        if args.subcommand == "delivery":
            resp = self.delivery(args.date)
            print(resp)
            return

    def followers(self, date):
        api = self.get_api_client()
        insight = api.get_insight_followers(date)
        return insight

    def delivery(self, date):
        api = self.get_api_client()
        insight = api.get_insight_message_delivery(date)
        return insight
        
