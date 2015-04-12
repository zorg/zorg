from zorg.adaptor import Adaptor
import mraa


MIN_PULSE_WIDTH = 600
MAX_PULSE_WIDTH = 2600
MAX_PERIOD = 7968


class Edison(Adaptor):

    def __init__(self, options):
        super(Edison, self).__init__(options)

        self.pins = {
            "digital": {},
            "analog": {},
            "pwm": {},
        }

        print "Edison"

    def servo_write(self, pin, degrees):

        pulse_width = MIN_PULSE_WIDTH + (degrees / 180.0) * (MAX_PULSE_WIDTH - MIN_PULSE_WIDTH)

        self.pwm_write(pin, int(pulse_width), MAX_PERIOD)

    def pwm_write(self, pin_number, value, period):

        if not pin_number in self.pins["pwm"]:
            pin = mraa.Pwm(pin_number)
            self.pins["pwm"][pin_number] = pin
            pin.period_us(period)
            
            pin.enable(True)
        else:
            pin = self.pins["pwm"][pin_number]

        pin.pulsewidth_us(value)

    def digital_write(self, pin_number, value):

        if not pin_number in self.pins["digital"]:
            pin = mraa.Gpio(pin_number)
            self.pins["digital"][pin_number] = pin

        else:
            pin = self.pins["digital"][pin_number]

        pin.dir(mraa.DIR_OUT)
        pin.write(value)

    def analog_read(self, pin_number):

        if not pin_number in self.pins["analog"]:
            pin = mraa.Aio(pin_number)
            self.pins["analog"][pin_number] = pin
        else:
            pin = self.pins["analog"][pin_number]

        return pin.read()
