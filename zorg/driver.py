class Driver(object):

    def __init__(self, options, connection):
        self.name = options.get("name", "")
        self.connection_name = options.get("connection", "")
        self.pin = options.get("pin", None)
        self.interval = options.get("interval", 10)

        self.connection = connection

        self.commands = []
        self.events = []

    def start(self):
        raise Exception("This needs to be implemented by the child class")

    def halt(self):
        raise Exception("This needs to be implemented by the child class")

    def serialize(self):
        return {
            "name": self.name,
            "pin": self.pin,
            "connection": self.connection_name,
            "commands": self.commands,
            "events": self.events,
        }
