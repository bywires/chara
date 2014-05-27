from unittest import TestCase
from tempfile import TemporaryFile

from .fixtures import Value
from chara import record, replay


MODULE = 'tests.test_decorators'


class DecoratorsTest(TestCase):
    def test_record_and_replay(self):
        target =  MODULE + '.Value'

        @record(target)
        def test(self):
            v = Value()
            v.value = 5
            self.assertEqual(5, v.get())

        test(self)

        @replay(target)
        def test(self):
            v = Value()
            self.assertEqual(5, v.get())

        test(self)

        self.fail()
