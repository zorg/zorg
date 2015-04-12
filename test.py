import zorg

def work(my):

    my.lock.set_angle(100)

    print "yours"

robot = zorg.robot({
    "connections": {
        "edison": {
            "adaptor": "zorg_edison.Edison"
        }
    },
    "devices": {
        "lock": {
            "driver": "zorg_gpio.Servo",
            "connection": "edison",
            "pin": 5
        }
    },
    "name": "Smith",
    "work": work
})

robot.start()
