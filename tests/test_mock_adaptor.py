from unittest import TestCase
from zorg.test import MockAdaptor


class MockAdaptorTestCase(TestCase):

    def setUp(self):
        super(MockAdaptorTestCase, self).setUp()

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

    def test_read_non_existing_pin(self):
        value = self.adaptor.digital_read(2)
        self.assertEqual(value, 0)

    def test_write_existing_pin(self):
        value = self.adaptor.digital_write(1, 0)
        self.assertEqual(value, 0)

    def test_write_non_existing_pin(self):
        value = self.adaptor.digital_write(2, 1)
        self.assertEqual(value, 1)
