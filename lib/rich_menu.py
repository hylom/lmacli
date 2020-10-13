"""LINE Message API: rich menu related API"""

from linebot.models import RichMenu
import json
import mimetypes

from .interface import Interface

class RichMenuInterface(Interface):
    def set_parser(self, name, subparsers):
        menu = subparsers.add_parser(name)
        menu_subp = menu.add_subparsers(dest='subcommand')
        menu_create = menu_subp.add_parser('create')
        menu_create.add_argument('menu',
                                 metavar='JSON_FILE',
                                 type=argparse.FileType('r'),
                                 help='JSON file to describe menu structure')
        menu_create.add_argument('-i', '--image',
                                 metavar='IMAGE_FILE',
                                 type=argparse.FileType('rb'),
                                 help='image file to upload')
        menu_create.add_argument('--content-type',
                                 help='content-type of image')
        menu_list = menu_subp.add_parser('list')
        menu_delete = menu_subp.add_parser('delete')
        menu_delete.add_argument('menu_id',
                                 help='rich menu ID to delete')
        menu_default = menu_subp.add_parser('setdefault')
        menu_default.add_argument('menu_id',
                                 help='rich menu ID to delete')
        menu_link = menu_subp.add_parser('link')
        menu_link.add_argument('user_id',
                                 help='user ID to attach rich menu')
        menu_link.add_argument('menu_id',
                                 help='rich menu ID')
        menu_unlink = menu_subp.add_parser('unlink')
        menu_unlink.add_argument('user_id',
                                 help='user ID to attach rich menu')
        menu_image = menu_subp.add_parser('image')
        menu_image_subp = menu_image.add_subparsers(dest='action')
        menu_image_upload = menu_image_subp.add_parser('upload')
        menu_image_upload.add_argument('rich_menu_id',
                                       metavar='rich-menu-id',
                                       help='rich menu id')
        menu_image_upload.add_argument('image',
                                       metavar='IMAGE_FILE',
                                       type=argparse.FileType('rb'),
                                       help='image file to upload')
        menu_image_upload.add_argument('--content-type',
                                       help='content-type of image')

    def execute(self, args):
        if args.subcommand == 'create':
            menu_data = json.load(args.menu)
            args.menu.close()
            resp = self.create(menu_data, args.image)
            print(resp)
            return
        elif args.subcommand == 'list':
            resp = self.list()
            print(resp)
            return
        elif args.subcommand == 'delete':
            resp = self.delete(args.menu_id)
            print(resp)
            return
        elif args.subcommand == 'link':
            resp = self.link(args.user_id, args.menu_id)
            print(resp)
            return
        elif args.subcommand == 'unlink':
            resp = self.unlink(args.user_id)
            print(resp)
            return
        elif args.subcommand == 'setdefault':
            resp = self.set_default(args.menu_id)
            print(resp)
            return
        elif args.subcommand == 'image':
            if args.action == 'upload':
                resp = self.upload_image(args.rich_menu_id,
                                         args.image)
                print(resp)
                return

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
        
