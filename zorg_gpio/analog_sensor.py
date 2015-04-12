from zorg.driver import Driver


class AnalogSensor(Driver):

    def __init__(self, options, connection):
        super(AnalogSensor, self).__init__(options, connection)

    def read(self):
        return self.connection.analog_read(self.pin)

