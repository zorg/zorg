from .utils import import_class


class Device(object):

    def __init__(self, options, connection):
        self.name = options.get("name", "")
        self.connection = connection

        driver_name = options.get("driver")

        driver_class = import_class(driver_name)

        self.driver = driver_class(options, connection)

    def __getattr__(self, name):
        return getattr(self.driver, name)

    def start_process(self):
        pass

    def on(self):
        pass
