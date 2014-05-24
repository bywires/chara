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
            Spy(MODULE + '.Dummy.dummy_instance_method'), 
            lambda: Dummy().dummy_instance_method
        )

    def test_spy_on_class_method(self):
        self.spy_on(
            Spy(MODULE + '.Dummy.dummy_class_method'), 
            lambda: Dummy.dummy_class_method
        )

    def test_spy_on_static_method(self):
        self.spy_on(
            Spy(MODULE + '.Dummy.dummy_static_method'), 
            lambda: Dummy.dummy_static_method
        )

    def spy_on(self, spy, getter):
        # shouldn't record this
        self.assertEqual(26, getter()(5, b=6, c=7, d=8), 
                         'Function didn\'t work before spying')

        with spy.record():
            target = getter()
            self.assertEqual(spy.attribute_name, target.__name__, 
                             'Function name not preserved')
            self.assertEqual(10, target(1, b=2, c=3, d=4),
                             'Function didn\t work during spying')

        # shouldn't record this
        self.assertEqual(26, getter()(5, b=6, c=7, d=8),
                         'Function didn\'t work after spying')

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
    def dummy_instance_method(self, a, b=0, *args, **kwargs):
        return dummy_function(a, b=b, *args, **kwargs)

    @classmethod
    def dummy_class_method(cls, a, b=0, *args, **kwargs):
        return dummy_function(a, b=b, *args, **kwargs)

    @staticmethod
    def dummy_static_method(a, b=0, *args, **kwargs):
        return dummy_function(a, b=b, *args, **kwargs)

