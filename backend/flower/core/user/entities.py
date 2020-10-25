from zope.interface import implementer
from ..common.ports import JsonfyPort


@implementer(JsonfyPort)
class UserEntity:
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def jsonify(self):
        return {
            'id': self.id,
            'username': self.username,
        }
