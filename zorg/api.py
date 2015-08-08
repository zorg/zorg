from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json


class Api(object):

    def __init__(self, options):
        self.commands = []
        self.events = []

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

        self.send_response(200)

        path_parts = filter(len, self.path.split("/"))

        try:
            response = self.get_response(path_parts)
        except Exception as ex:
            print traceback.format_exc()

            response = self.handle_error(ex)

        json_response = json.dumps(response)

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
            raise Exception("This page could not be found.")

        if hasattr(self, method_name):
            method = getattr(self, method_name)

            return method(*arguments)

        return {}

    def handle_error(self, exception):
        return {
            "error": str(exception),
        }

    def handle_api(self):
        response = {
            "commands": self.server.api.commands,
            "events": self.server.api.events,
        }

        response.update(self.handle_robots())

        return {
            "MCP": response,
        }

    def handle_commands(self, command_name=None):
        if command_name:
            return self.handle_command(command_name)

        response = {
            "commands": self.server.api.commands,
        }

        return response

    def handle_command(self, command_name):
        command = getattr(self.server.api, command_name)

        command_arguments = self.parse_command_body()

        result = command(*command_arguments)

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
            "commands": robot.commands,
        }

        return response

    def handle_robot_command(self, robot_name, command_name):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        command = getattr(robot, command_name)

        command_arguments = self.parse_command_body()

        result = command(*command_arguments)

        return {
            "result": result,
        }

    def handle_robots_connections(self, robot_name, connection_name=None):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        if connection_name:
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
            "commands": device.commands,
        }

    def handle_robot_device_command(
        self, robot_name, device_name, command_name
    ):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        device = getattr(robot.helper, device_name)

        command = getattr(device, command_name)

        command_arguments = self.parse_command_body()

        result = command(*command_arguments)

        return {
            "result": result,
        }

    def handle_robots_devices_events(
        self, robot_name, device_name, event_name=None
    ):
        from zorg import main

        if event_name:
            return {}

        robots = main.robots
        robot = robots[robot_name]

        device = getattr(robot.helper, device_name)

        return {
            "events": device.events,
        }

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

    def start(self):
        server = HTTPServer(('0.0.0.0', 8000), HttpRequestHandler)
        server.api = self
        server.serve_forever()
