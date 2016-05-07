from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json


class Api(object):

    def __init__(self, options):
        pass

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
            print(traceback.format_exc())

            response = {
                "error": str(ex),
            }

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
        if not path or path[0] != "api":
            return {}

        if len(path) == 1:
            return self.handle_api()

        if len(path) == 2 and path[1] == "robots":
            return self.handle_robots()

        if len(path) == 3 and path[1] == "robots":
            return self.handle_robot(path[2])

        if len(path) == 4 and path[1] == "robots":
            if path[3] == "devices":
                return self.handle_robot_devices(path[2])

        if len(path) == 5 and path[1] == "robots":
            if path[3] == "devices":
                return self.handle_robot_device(path[2], path[4])

        if len(path) == 6 and path[1] == "robots":
            if path[3] == "devices":
                if path[5] == "commands":
                    return self.handle_robot_device_commands(path[2], path[4])

                if path[5] == "events":
                    return self.handle_robot_device_events(path[2], path[4])

        if len(path) == 7 and path[1] == "robots":
            if path[3] == "devices":
                if path[5] == "commands":
                    return self.handle_robot_device_command(
                        path[2], path[4], path[6]
                    )

        return {}

    def handle_api(self):
        response = {
            "commands": [],
            "events": [],
        }

        response.update(self.handle_robots())

        return {
            "MCP": response,
        }

    def handle_robots(self):
        from zorg import main

        robots = main.robots

        response = {
            "robots": [],
        }

        for robot_name, robot in robots.items():
            serialized = robot.serialize()

            response["robots"].append(serialized)

        return response

    def handle_robot(self, name):
        from zorg import main

        robots = main.robots
        robot = robots[name]

        response = {
            "robot": robot.serialize(),
        }

        return response

    def handle_robot_devices(self, name):
        from zorg import main

        robots = main.robots
        robot = robots[name]

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

    def handle_robot_device_commands(self, robot_name, device_name):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        device = getattr(robot.helper, device_name)

        return {
            "commands": device.commands,
        }

    def handle_robot_device_events(self, robot_name, device_name):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        device = getattr(robot.helper, device_name)

        return {
            "events": device.events,
        }

    def handle_robot_device_command(
            self, robot_name, device_name, command_name):
        from zorg import main

        robots = main.robots
        robot = robots[robot_name]

        device = getattr(robot.helper, device_name)

        command = getattr(device, command_name)

        if self.method == "GET":
            request_body = ""
        else:
            request_body = self.rfile.read(
                int(self.headers.getheader('content-length'))
            )

        if request_body:
            args = json.loads(request_body)
        else:
            args = {}

        result = command(**args)

        return {
            "result": result,
        }


class Http(Api):

    def start(self):
        server = HTTPServer(('0.0.0.0', 8000), HttpRequestHandler)
        server.serve_forever()
