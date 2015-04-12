import time
import zorg


def move_servo(my):
    angle = 0

    while True:
        my.servo.set_angle(angle)

        angle += 45

        if angle > 135:
            angle = 0

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
            "driver": "zorg_gpio.Servo",
            "pin": 5, # Digital/PWM pin 5
        },
    },
    "work": move_servo,
})

robot.start()
