from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from .commands import CommandsMixin
from .events import EventsMixin
import json


class Http404(Exception):
    pass


class ResponseFinished(Exception):
    pass


class Api(CommandsMixin, EventsMixin):

    def __init__(self, options):
        super(Api, self).__init__()

    def start(self):
        pass

    def halt(self):
        pass


class HttpRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(204)

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        import traceback

        if not hasattr(self, "method"):
            self.method = "GET"

        path_parts = filter(len, self.path.split("/"))

        status_code = 200

        try:
            response = self.get_response(path_parts)
        except Exception as ex:
            print traceback.format_exc()

            response = self.handle_error(ex)

            if isinstance(ex, Http404):
                status_code = 404
            elif isinstance(ex, ResponseFinished):
                return
            else:
                status_code = 500

        json_response = json.dumps(response)

        self.send_response(status_code)

        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_response))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        self.wfile.write(json_response)
        self.wfile.close()

    def do_POST(self):
        self.method = "POST"

        return self.do_GET()

    def get_response(self, path):
        if not path:
            return self.handle_error(path)

        method_name = path[0]
        arguments = []

        if len(path) > 1:
            method_parts = path[1::2]
            arguments = path[2::2]

            method_name = "handle_" + "_".join(method_parts)
        elif len(path) == 1 and path[0] == "api":
            return self.handle_api()
        else:
            raise Http404("This page could not be found.")

        if hasattr(self, method_name):
            method = getattr(self, method_name)

            return method(*arguments)

        return {}

    def handle_error(self, exception):
        return {
            "error": str(exception),
        }

    def handle_api(self):
        response = self.server.api.serialize()

        response.update(self.handle_robots())

        return {
            "MCP": response,
        }

    def handle_commands(self, command_name=None):
        if command_name:
            return self.handle_command(command_name)

        response = {
            "commands": self.server.api.serialize_commands(),
        }

        return response

    def handle_command(self, command_name):
        if command_name not in self.server.api.serialize_commands():
            raise Http404()

        command_arguments = self.parse_command_body()

        result = self.server.api.run_command(command_name, command_arguments)

        return {
            "result": result,
        }

    def handle_robots(self, robot_name=None):
        from zorg import main

        if robot_name:
            return self.handle_robot(robot_name)

        robots = main.robots

        response = {
            "robots": [],
        }

        for robot_name, robot in robots.items():
            serialized = robot.serialize()

            response["robots"].append(serialized)

        return response

    def handle_robot(self, robot_name):
        from zorg import main

        robots = main.robots

        if robot_name not in robots:
            raise Http404("No robot found with the name %s" % robot_name)

        robot = robots[robot_name]

        response = {
            "robot": robot.serialize(),
        }

        return response

    def handle_robots_commands(self, robot_name, command_name=None):
        from zorg import main

        if command_name:
            return self.handle_robot_command(robot_name, command_name)

        robots = main.robots
        robot = robots[robot_name]

        response = {
            "commands": robot.serialize_commands(),
        }

        return response

    def handle_robot_command(self, robot_name, command_name):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        command_arguments = self.parse_command_body()

        result = robot.run_command(command_name, command_arguments)

        return {
            "result": result,
        }

    def handle_robots_connections(self, robot_name, connection_name=None):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        if connection_name:
            if connection_name not in robot.connections:
                raise Http404(
                    "No connection found with the name %s" % connection_name
                )

            connection = robot.helper.initialize_connection(connection_name)

            response = {
                "connection": connection.serialize(),
            }
        else:
            connections = robot.serialize_connections()

            response = {
                "connections": connections,
            }

        return response

    def handle_robots_devices(self, robot_name, device_name=None):
        from zorg import main

        if device_name:
            return self.handle_robot_device(robot_name, device_name)

        robots = main.robots
        robot = robots[robot_name]

        response = {
            "devices": robot.serialize_devices(),
        }

        return response

    def handle_robot_device(self, robot_name, device_name):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        if not hasattr(robot.helper, device_name):
            raise Http404("No device found with the name %s" % device_name)

        device = getattr(robot.helper, device_name)

        return {
            "device": device.serialize()
        }

    def handle_robots_devices_commands(
        self, robot_name, device_name, command_name=None
    ):
        from zorg import main

        if command_name:
            return self.handle_robot_device_command(
                robot_name, device_name, command_name
            )

        robots = main.robots
        robot = robots[robot_name]

        device = getattr(robot.helper, device_name)

        return {
            "commands": device.serialize_commands(),
        }

    def handle_robot_device_command(
        self, robot_name, device_name, command_name
    ):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        device = getattr(robot.helper, device_name)

        command_arguments = self.parse_command_body()

        result = device.run_command(command_name, *command_arguments)

        return {
            "result": result,
        }

    def handle_robots_devices_events(
        self, robot_name, device_name, event_name=None
    ):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        device = getattr(robot.helper, device_name)

        if event_name:
            event_stream = device.get_event_stream(event_name)

            return self.handle_event_stream(event_stream)

        return {
            "events": device.serialize_events(),
        }

    def handle_robots_events(self, robot_name, event_name=None):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        if event_name:
            event_stream = robot.get_event_stream(event_name)

            return self.handle_event_stream(event_stream)

        return {
            "events": robot.serialize_events()
        }

    def handle_event_stream(self, event_stream):
        from zorg.events import Event

        queue = event_stream.queue

        self.send_response(200)
        self.send_header('content-type', 'text/event-stream')
        self.end_headers()

        try:
            for event in iter(queue.get, Event.STOP):
                self.wfile.write(event.serialize())
        except IOError:
            # If the client closes the stream, move on
            pass

        event_stream.stop()

        raise ResponseFinished()

    def parse_command_body(self):
        from collections import OrderedDict

        if self.method == "GET":
            request_body = ""
        else:
            request_body = self.rfile.read(
                int(self.headers.getheader('content-length'))
            )

        if not request_body:
            return []

        command_arguments = json.loads(
            request_body,
            object_pairs_hook=OrderedDict,
        )

        return command_arguments.values()


class Http(Api):

    def start_server(self):
        server = HTTPServer(('0.0.0.0', 8000), HttpRequestHandler)
        server.api = self
        server.serve_forever()

    def start(self):
        process = Process(target=self.start_server)

        process.start()
        return process
