from .utils import import_class
from .adaptor import Adaptor


class Connection(object):

    def __init__(self, options):

        adaptor_name = options.get("adaptor")

        adaptor_class = import_class(adaptor_name)

        self.adaptor = adaptor_class(options)

    def __getattr__(self, name):
        return getattr(self.adaptor, name)
