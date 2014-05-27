from unittest import TestCase
from tempfile import TemporaryFile

from .fixtures import Value
from chara import record, replay
from chara.exceptions import CallNotFoundException


MODULE = 'tests.test_integration'


class IntegrationTest(TestCase):
    def test_record_and_replay_sequence(self):
        target =  MODULE + '.Value'

        @record(target)
        def test(self):
            v = Value()
            v.value = 5
            self.assertEqual(5, v.get())
            v.value = 10
            self.assertEqual(10, v.get())

        test(self)

        @replay(target)
        def test(self):
            v = Value()
            self.assertEqual(5, v.get())
            self.assertEqual(10, v.get())

            with self.assertRaises(CallNotFoundException):
                v.get()

        test(self)
