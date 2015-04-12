from .robot import Robot

robots = {}

def robot(options):
    name = options["name"]

    if name in robots:
        raise Exception("The robot's name must be unique")

    robot = Robot(options)

    robots[name] = robot

    return robot
