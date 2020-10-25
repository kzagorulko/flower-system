import zope.interface

class JsonfyPort(zope.interface.Interface):
    def jsonfy(self):
        """Return json object representation"""