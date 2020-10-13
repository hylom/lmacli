"""LINE Message API: audience managing related API"""

from linebot.models import TextSendMessage
import urllib
import json

from .interface import Interface

class AudienceInterface(Interface):
    def set_parser(self, name, subparsers):
        aud = subparsers.add_parser(name)
        aud_subparsers = aud.add_subparsers(dest='subcommand')
        aud_list = aud_subparsers.add_parser('list')

    def execute(self, args):
        if args.subcommand == "list":
            resp = self.list()
            print(resp)
            return

    def create_upload(self,
                      ids,
                      description,
                      upload_description="",
                      is_ifa_audience=False):
        audiences = [ dict(id=x) for x in ids ]
        data = {
            'description': description,
            'isIfaAudience': is_ifa_audience,
            'uploadDescription': upload_description,
            'audiences': audiences,
        }
        response = self.get_api_client()._post(
            '/v2/bot/audienceGroup/upload',
            data=json.dumps(data, sort_keys=True),
            headers={'Content-Type': 'application/json'},
            timeout=timeout
        )
        return response.json.get('audienceGroupId')

    def list(self,
             page=1,
             description="",
             status="",
             size=20,
             includes_external_public_groups="",
             create_route=""):
        data = {
            "page": page,
            "description": description,
            "status": status,
            "size": size,
            "includeExternalpublicGroups": includes_external_public_groups,
            "createRoute": create_route,
        }
        url = '/v2/bot/audienceGroup/list?' + urllib.parse.urlencode(data)
        response = self.get_api_client()._get(url)
        return response.json
