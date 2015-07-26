import zorg

robot = zorg.robot({
    "name": "TestBot",
    "work": None,
})

api = zorg.api("zorg.api.Http", {})

def echo(message=None):
    if message is None:
        return "No value passed to echo"

    return message

api.commands += ['echo']
api.echo = echo

robot.start()
api.start()
