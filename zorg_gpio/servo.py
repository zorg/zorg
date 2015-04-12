from zorg.driver import Driver


class Servo(Driver):

    def __init__(self, options, connection):
        super(Servo, self).__init__(options, connection)

        self.angle = -1
        self.commands += ["set_angle", "get_angle"]

        print "servo"

    def set_angle(self, angle):

        self.angle = angle
        self.connection.servo_write(self.pin, angle)

    def get_angle(self):
        return self.angle
