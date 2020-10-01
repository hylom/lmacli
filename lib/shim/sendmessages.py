
from linebot.models import SendMessage
from linebot.models.emojis import Emojis

class TextSendMessage(SendMessage):
    """TextSendMessage.
    https://developers.line.biz/en/reference/messaging-api/#text-message
    """

    def __init__(self, text=None, emojis=None, quick_reply=None, **kwargs):
        """__init__ method.
        :param str text: Message text
        :param quick_reply: QuickReply object
        :type quick_reply: T <= :py:class:`linebot.models.send_messages.QuickReply`
        :param kwargs:
        """
        super(TextSendMessage, self).__init__(quick_reply=quick_reply, **kwargs)

        self.type = 'text'
        self.text = text
        if emojis:
            new_emojis = []
            for emoji in emojis:
                emoji_object = self.get_or_new_from_json_dict(
                    emoji, Emojis
                )
                if emoji_object:
                    new_emojis.append(emoji_object)
            self.emojis = new_emojis
        self.emojis = emojis
