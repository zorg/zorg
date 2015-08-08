class Driver(object):

    def __init__(self, options, connection):
        self.name = options.get("name", "")
        self.connection_name = options.get("connection", "")
        self.pin = options.get("pin", None)
        self.interval = options.get("interval", 10)

        self.options = options

        self.connection = connection

        self.commands = []
        self.events = []

    def start(self):
        raise Exception("This needs to be implemented by the child class")

    def halt(self):
        raise Exception("This needs to be implemented by the child class")

    def serialize(self):
        details = self.options.copy()

        if "name" in details:
            del details["name"]

        if "connection" in details:
            del details["connection"]

        driver = details.pop("driver", "")
        driver = driver.split(".")[-1]

        return {
            "name": self.name,
            "driver": driver,
            "connection": self.connection_name,
            "commands": self.commands,
            "events": self.events,
            "details": details,
        }


class Ping(Driver):

    def __init__(self, *args, **kwargs):
        super(Ping, self).__init__(*args, **kwargs)

        self.commands += ['ping']

    def ping(self):
        return "pong"
