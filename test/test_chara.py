from unittest import TestCase

from chara import Spy, Call

class CharaTest(TestCase):
    def test_spy_on_function(self):
        spy = Spy('chara.test.test_chara.dummy')

        # shouldn't record this
        self.assertEqual(15, dummy(4, b=5, c=6))

        with spy.record():
            self.assertEqual(6, dummy(1, b=2, c=3))

        # shouldn't record this
        self.assertEqual(15, dummy(4, b=5, c=6))

        self.assertEqual(
            spy.calls[0], 
            Call(args=(1, 2), kwargs={'c': 3}, return_value=6)
        )

        self.assertEqual(1, len(spy.calls))


def dummy(a, b=0, **kwargs):
    return a + b + sum(kwargs.values())


class Dummy(object):
    def dummy(self, a, b=0, **kwargs):
        return a + b + sum(kwargs.values())
