from unittest import TestCase
from tempfile import TemporaryFile

from .fixtures import Value, Cache
from chara import record, replay, storage
from chara.exceptions import CallNotFoundException


MODULE = 'tests.test_integration'


class IntegrationTest(TestCase):
    def setUp(self):
        # clean up anything from last test
        def test_sequence(self):
            pass

        storage.delete(test_sequence, self)

    def test_record_and_replay_sequence(self):
        target =  MODULE + '.Value'

        @record(target)
        def test_sequence(self):
            v = Value()
            v.value = 5
            self.assertEqual(5, v.get())
            v.value = 10
            self.assertEqual(10, v.get())

        test_sequence(self)

        @replay(target)
        def test_sequence(self):
            v = Value()
            self.assertEqual(5, v.get())
            self.assertEqual(10, v.get())

            with self.assertRaises(CallNotFoundException):
                v.get()

        test_sequence(self)

    def test_record_and_replay_pattern_matching(self):
        target =  MODULE + '.Cache'

        @record(target)
        def test_pattern_matching(self):
            c = Cache()
            c.set('five', 5)
            self.assertEqual(5, c.get('five'))
            c.set('ten', 10)
            self.assertEqual(10, c.get('ten'))

        test_pattern_matching(self)

        @replay(target, pattern_match_mode=True)
        def test_pattern_matching(self):
            c = Cache()
            self.assertEqual(10, c.get('ten'))
            self.assertEqual(5, c.get('five'))
            self.assertEqual(5, c.get('five'))
            self.assertEqual(10, c.get('ten'))

        test_pattern_matching(self)
