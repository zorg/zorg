# Testing with Zorg

Automated testing is extremely beneficial to ensure that your
creations function as expected under various conditions. By
creating a set of tests to accompany your code you can avoid
a number of common problems.

1. When you are creating new code, your tests will ensure that your code works as expected.
2. When you, or others are modifying existing code, your tests will help verify that unanticipated changes have not occured.

Because of the complexity of testing robotics and physical computing projects, Zorg aims to include testing utilities that ease and assist with test creation.

The preferred way to write tests for Zorg is with the [unittest](https://docs.python.org/3/library/unittest.html#module-unittest) module built in to the Python standard library.

## Mock objects

Mock objects can simulate hardware responses so that your tests
can run independent of various hardware constraints.

### `MockAdaptor`

The mock adaptor simulates an `Adaptor` class in the Zorg framework. The constructor for the mock adapter allows you
to specify the available pins and their returned output value.
The methods available to call on the adapter can also be set.

**Example usage of the MockAdaptor**

```python
from unittest import TestCase
from zorg.test import MockAdaptor


class MockAdaptorTestCase(TestCase):

    def setUp(self):
        super(MockAdaptorTestCase, self).setUp()

        # outputs = {pin: output value}
        self.adaptor = MockAdaptor({
            'outputs': {
                1: 1,
                3: 1.0,
                4: 500,
                9: 0
            },
            'methods': ['digital_read', 'digital_write']
        })

    def test_read_existing_pin(self):
        value = self.adaptor.digital_read(1)
        self.assertEqual(value, 1)
```


