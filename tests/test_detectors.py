from unittest import TestCase

from .fixtures import Dummy
from chara.detectors import get_callables


class GetCallablesTest(TestCase):
    def setUp(self):
        self.callables = get_callables(Dummy)

    def test_instance_method(self):
        self.assertEqual(
            Dummy.dummy_instance_method, 
            self.callables.get('dummy_instance_method')
        )

    def test_class_method(self):
        self.assertEqual(
            Dummy.dummy_class_method, 
            self.callables.get('dummy_class_method')
        )

    def test_static_method(self):
        self.assertEqual(
            Dummy.dummy_static_method, 
            self.callables.get('dummy_static_method')
        )

    def test_exclude_non_callable(self):
        self.assertNotIn('dummy_attribute', self.callables)

