"""LINE Message API: rich menu related API"""

from linebot.models import RichMenu
import json
import mimetypes

from .interface import Interface

class RichMenuInterface(Interface):
    def create(self, menu, image, content_type=None):
        api = self.get_api_client()
        menu_obj = RichMenu.new_from_json_dict(menu)

        resp = api.create_rich_menu(menu_obj)

        if image and resp:
            resp2 = self.upload_image(resp, image, content_type)
        return resp
            
    def list(self):
        api = self.get_api_client()
        resp = api.get_rich_menu_list()
        return resp

    def set_default(self, menu_id):
        api = self.get_api_client()
        resp = api.set_default_rich_menu(menu_id)
        return resp
        
    def delete(self, menu_id):
        api = self.get_api_client()
        resp = api.delete_rich_menu(menu_id)
        return resp

    def link(self, user_id, menu_id):
        api = self.get_api_client()
        resp = api.link_rich_menu_to_user(user_id, menu_id)
        return resp

    def unlink(self, user_id):
        api = self.get_api_client()
        resp = api.unlink_rich_menu_from_user(user_id)
        return resp

    def upload_image(self, menu_id, fp, content_type=None):
        api = self.get_api_client()
        if fp.name and not content_type:
            (type, enc) = mimetypes.guess_type(fp.name)
            if type:
                content_type = type
        if not content_type:
            raise Execption("no content_type")
            
        resp = api.set_rich_menu_image(menu_id, content_type, fp)
        return resp
        
