"""LINE Message API: insight related API"""

import json

from .interface import Interface

class InsightInterface(Interface):
    def followers(self, date):
        api = self.get_api_client()
        insight = api.get_insight_followers(date)
        return insight

    def delivery(self, date):
        api = self.get_api_client()
        insight = api.get_insight_message_delivery(date)
        return insight
        
