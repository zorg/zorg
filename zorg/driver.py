from .events import EventsMixin


class Driver(EventsMixin):

    def __init__(self, options, connection):
        super(Driver, self).__init__()

        self.name = options.get("name", "")
        self.connection_name = options.get("connection", "")
        self.pin = options.get("pin", None)
        self.interval = options.get("interval", 10)

        if self.pin:
            options["pin"] = str(self.pin)

        self.options = options

        self.connection = connection

        self.commands = []

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

        serialized = super(Driver, self).serialize()

        serialized.update({
            "name": self.name,
            "driver": driver,
            "connection": self.connection_name,
            "commands": self.commands,
            "details": details,
        })

        return serialized


class Ping(Driver):

    def __init__(self, *args, **kwargs):
        super(Ping, self).__init__(*args, **kwargs)

        self.commands += ["ping"]
        self.events["ping"] = {
            "source": self.ping,
            "interval": 0.1,
        }

    def start(self):
        pass

    def ping(self):
        return "pong"
