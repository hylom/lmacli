"""LINE Message API: push related API"""

from linebot.models import TextSendMessage, AudienceRecipient, Filter, Limit
import json

from .interface import Interface

class PushInterface(Interface):

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
        
