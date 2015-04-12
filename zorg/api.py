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

    def do_GET(self):
        self.send_response(200)

        json_data = json.dumps({
            "path": self.path,
        })

        path_parts = filter(len, self.path.split("/"))

        response = self.get_response(path_parts)
        json_response = json.dumps(response)

        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_response))
        self.end_headers()

        self.wfile.write(json_response)
        self.wfile.close()

    def get_response(self, path):
        if not path or path[0] != "api":
            return {}

        if len(path) == 1:
            return self.handle_api()

        return {}

    def handle_api(self):
        from zorg import main

        robots = main.robots

        response = {
            "robots": [],
        }

        for robot_name, robot in robots.items():
            serialized = robot.serialize()

            response["robots"].append(serialized)

        return response

class Http(Api):

    def start(self):
        server = HTTPServer(('0.0.0.0', 8000), HttpRequestHandler)
        server.serve_forever()
