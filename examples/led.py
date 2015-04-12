import time
import zorg


def blink_led(my):
    while True:
        my.led.toggle()
        time.sleep(100)

robot = zorg.robot({
    "name": "Test",
    "connections": {
        "edison": {
            "adaptor": "zorg_edison.Edison",
        },
    },
    "devices": {
        "led": {
            "connection": "edison",
            "driver": "zorg_gpio.Led",
            "pin": 4, # Digital pin 4
        },
    },
    "work": blink_led,
})

robot.start()
