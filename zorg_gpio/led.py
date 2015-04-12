from zorg.driver import Driver


class Led(Driver):

    def __init__(self, options, connection):
        super(Led, self).__init__(options, connection)

        self.is_on = False

    def set_state(self, state):
        """
        State should be a 1 or a 0.
        """
        self.is_on = state
        self.connection.digital_write(self.pin, state)

    def is_on(self):
        return self.is_on

    def turn_on(self):
        self.is_on = True
        self.connection.digital_write(self.pin, 1)

    def turn_off(self):
        self.is_on = False
        self.connection.digital_write(self.pin, 0)

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()
