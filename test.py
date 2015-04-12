import zorg

def work(my):

    #my.lock.set_angle(100)

    import time
    while True:
        my.led.toggle()
        time.sleep(1)

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
        },
        "led": {
            "driver": "zorg_gpio.Led",
            "connection": "edison",
            "pin": 4
        }
    },
    "name": "Smith",
    "work": work
})

robot.start()
