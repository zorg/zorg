class Driver(object):

    def __init__(self, options, connection):
        self.name = options.get("name", "")
        self.connection = connection
        self.pin = options.get("pin", None)
        self.interval = options.get("interval", 10)

        self.commands = []
        self.events = []

    def start(self):
        raise Exception("This needs to be implemented by the child class")

    def halt(self):
        raise Exception("This needs to be implemented by the child class")
