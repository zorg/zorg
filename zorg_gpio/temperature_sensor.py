from .analog_sensor import AnalogSensor
import math


class TemperatureSensor(AnalogSensor):

    def __init__(self, options, connection):
        super(TemperatureSensor, self).__init__(options, connection)

        self.commands = ["read", "read_fahrenheit", "read_celsius", "read_kelvin"]

    def read_resistance(self):
        """
        Read and return the resistive value of the          
        temperature sensor.        
        """
        analog_value = self.read()
        return (1023 - analog_value) * 10000 / analog_value

    def read_celsius(self):
        """
        Read and return the celsius value of the
        temperature sensor.
        See data sheet:
        http://www.seeedstudio.com/wiki/images/a/a1/NCP18WF104F03RC.pdf
        """
        resistance = self.read_resistance()
        THERMISTOR_VALUE = 3975
        return 1 / (math.log(resistance / 10000) / THERMISTOR_VALUE + 1 / 298.15) - 273.15

    def read_fahrenheit(self):
        """
        Read and return the fahrenheit value of the
        temperature sensor.
        """
        return (self.read_celsius * 9.0 / 5.0) + 32

    def read_kelvin(self):
        """
        Read and return the kelvin value of the
        temperature sensor.
        """
        return self.read_celsius() + 273.15
