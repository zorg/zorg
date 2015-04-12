from .robot import Robot
from .utils import import_class


robots = {}


def robot(options):
    name = options["name"]

    if name in robots:
        raise Exception("The robot's name must be unique")

    robot = Robot(options)

    robots[name] = robot

    return robot


def api(class_path, options):
    api_class = import_class(class_path)

    api_instance = api_class(options)

    return api_instance
