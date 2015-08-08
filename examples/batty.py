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

def hello_event():
    return "hello"

robot.commands += ['hello']
robot.hello = hello

robot.events["hello"] = {
    "source": hello_event,
    "interval": 0.1,
}

api = zorg.api("zorg.api.Http", {})

def echo(message=None):
    if message is None:
        raise Exception("No value passed to echo")

    return message

api.commands += ['echo']
api.echo = echo

robot.start()
api.start()
