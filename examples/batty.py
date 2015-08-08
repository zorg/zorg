import zorg

robot = zorg.robot({
    "name": "TestBot",
    "work": None,
    "connections": {
        "loopback": {
            "adaptor": "zorg.adaptor.Loopback",
            "port": "/dev/null",
            "test": "abc",
        }
    },
    "devices": {
        "ping": {
            "connection": "loopback",
            "driver": "zorg.driver.Ping",
            "pin": 13,
            "test": "abc",
        }
    }
})

def hello(target):
    return "Hello, %s!" % target

robot.commands += ['hello']
robot.hello = hello

api = zorg.api("zorg.api.Http", {})

def echo(message=None):
    if message is None:
        return "No value passed to echo"

    return message

api.commands += ['echo']
api.echo = echo

robot.start()
api.start()
