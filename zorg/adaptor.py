class Adaptor(object):

    def __init__(self, options):
        self.name = options.get("name", "")
        self.host = options.get("host", None)
        self.port = options.get("port", None)

    def serialize(self):
        return {
            "name": self.name,
            "host": self.host,
            "port": self.port,
        }

    def connect(self):
        raise Exception("This needs to be overriden in child classes")

    def disconnect(self):
        raise Exception("This method needs to be overidden in child classes")
