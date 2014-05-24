from unittest import TestCase

from chara import Spy, Call

MODULE = 'tests.test_chara'

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
        self.assertEqual(26, getter()(5, b=6, c=7, d=8))

        with spy.record():
            self.assertEqual(10, getter()(1, b=2, c=3, d=4))

        # shouldn't record this
        self.assertEqual(26, getter()(5, b=6, c=7, d=8))

        self.assertEqual(
            spy.calls, 
            [ Call(
                args=(1, 2), 
                kwargs={'c': 3, 'd': 4}, 
                return_value=10
            ) ]
        )


def dummy_function(a, b=0, *args, **kwargs):
    return a + b + sum(args) + sum(kwargs.values())


class Dummy(object):
    @classmethod
    def dummy_classmethod(cls, a, b=0, *args, **kwargs):
        return dummy_function(a, b=b, *args, **kwargs)

    def dummy_instancemethod(self, a, b=0, *args, **kwargs):
        return dummy_function(a, b=b, *args, **kwargs)

