import zorg
import time

def work(my):
    my.lock.set_angle(50)

    while True:
        my.led.toggle()
        print my.mic.read()

        time.sleep(1)

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
        },
        "mic": {
            "driver": "zorg_gpio.AnalogSensor",
            "connection": "edison",
            "pin": 1
        }
    },
    "name": "Smith",
    "work": work
})

api = zorg.api("zorg.api.Http", {})

#robot.start()
api.start()
