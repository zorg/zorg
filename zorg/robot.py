from multiprocessing import Process
from .adaptor import Adaptor
from .connection import Connection
from .device import Device


class Helper(object):

    def __init__(self, devices, connections):
        self.devices = devices
        self.connections = connections

        self._devices = {}
        self._connections = {}

    def __getattr__(self, name):
        if name in self._devices:
            return self._devices[name]

        self._devices[name] = self.initialize_device(name)

        return self._devices[name]

    def initialize_device(self, name):
        device_config = self.devices[name]

        connection_name = device_config["connection"]

        if connection_name in self._connections:
            connection = self._connections[connection_name]
        else:
            connection = self.initialize_connection(connection_name)
            self._connections[connection_name] = connection

        device = Device(device_config, connection)

        return device

    def initialize_connection(self, name):
        connection_config = self.connections[name]

        connection = Connection(connection_config, name=name)

        return connection

class Robot(object):

    def __init__(self, options):
        self.name = options.get("name", "")
        self.connections = options.get("connections", {})
        self.adaptors = options.get("adaptors", {})
        self.devices = options.get("devices", {})

        self.drivers = {}

        self.commands = []
        self.events = []

        self.running = False

        self.work = options["work"]

    def start(self):
        helper = Helper(self.devices, self.connections)

        process = Process(target=self.work, args=(helper, ))

        process.start()
        return process

    def halt(self):
        pass

    def serialize(self):
        return {
            "name": self.name,
            "commands": self.commands,
            "events": self.events,
            "connections": self.serialize_connections()
        }

    def serialize_connections(self):
        connections = []

        for name, config in self.connections.items():
            connection = Connection(config, name=name)

            connections.append(connection.serialize())

        return connections
