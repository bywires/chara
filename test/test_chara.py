from unittest import TestCase

from chara import Spy, Call

MODULE = 'chara.test.test_chara'

class CharaTest(TestCase):
    def test_spy_on_function(self):
        self.spy_on(
            Spy(MODULE + '.dummy_function'), 
            lambda: dummy_function
        )

    def test_spy_on_instance_method(self):
        self.spy_on(
            Spy(MODULE + '.Dummy.dummy_instancemethod'), 
            lambda: Dummy().dummy_instancemethod
        )

    def test_spy_on_class_method(self):
        self.spy_on(
            Spy(MODULE + '.Dummy.dummy_classmethod'), 
            lambda: Dummy.dummy_classmethod
        )

    def spy_on(self, spy, getter):
        # shouldn't record this
        self.assertEqual(15, getter()(4, b=5, c=6))

        with spy.record():
            self.assertEqual(6, getter()(1, b=2, c=3))

        # shouldn't record this
        self.assertEqual(15, getter()(4, b=5, c=6))

        self.assertEqual(
            spy.calls, 
            [ Call(
                args=(1, 2), 
                kwargs={'c': 3}, 
                return_value=6
            ) ]
        )


def dummy_function(a, b=0, **kwargs):
    return a + b + sum(kwargs.values())


class Dummy(object):
    @classmethod
    def dummy_classmethod(cls, a, b=0, **kwargs):
        return a + b + sum(kwargs.values())

    def dummy_instancemethod(self, a, b=0, **kwargs):
        return a + b + sum(kwargs.values())
