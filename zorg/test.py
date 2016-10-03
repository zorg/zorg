from zorg.adaptor import Adaptor
from mock import Mock


def MockAdaptor(configuration):
    """
    :param configuration: A dictionary with keys of pin numbers and values as
    the return value from the method call.
    :param methods: A list of method names that can be called on the adapter.

    For example:

    configuration = {
        'outputs': {
            1: 500,
            3: 1.0,
            4: 150,
            9: 0
        },
        'methods': ['analog_write', 'analog_read', 'digital_write']
    }
    """
    outputs = configuration.get('outputs', {})
    methods = configuration.get('methods', [])

    def side_effect(*args):
        pin_number = args[0]
        if len(args) > 1:
            return args[1]
        elif args and pin_number in outputs:
            return outputs[pin_number]
        else:
            return 0

    mock_adaptor = Mock(spec=Adaptor)

    for method in methods:
        setattr(mock_adaptor, method, Mock(side_effect=side_effect))

    return mock_adaptor
