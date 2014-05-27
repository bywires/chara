from unittest import TestCase

from .fixtures import dummy_function, Dummy
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

    def test_all_class_methods(self):
        spy = Spy(MODULE + '.Dummy')

        with spy.record():
            Dummy.dummy_class_method(1, b=2, c=3, d=4)
            Dummy.dummy_static_method(5, b=6, c=7, d=8)
            Dummy().dummy_instance_method(9, b=10, c=11, d=12)

        self.assertEqual(
            spy.calls, 
            {
                'dummy_class_method': [
                    Call(
                        args=(1, 2), 
                        kwargs={'c': 3, 'd': 4}, 
                        return_value=10
                    )
                ],

                'dummy_static_method': [
                    Call(
                        args=(5, 6), 
                        kwargs={'c': 7, 'd': 8}, 
                        return_value=26
                    )
                ],

                'dummy_instance_method': [
                    Call(
                        args=(9, 10), 
                        kwargs={'c': 11, 'd': 12}, 
                        return_value=42
                    )
                ]
            }
        )        

    def spy_on(self, spy, getter):
        # shouldn't record this
        self.assertEqual(26, getter()(5, b=6, c=7, d=8), 
                         'Function didn\'t work before spying')

        with spy.record() as call_list:
            target = getter()
            self.assertEqual(spy.name, target.__name__, 
                             'Function name not preserved')
            self.assertEqual(10, target(1, b=2, c=3, d=4),
                             'Function didn\'t work during spying')

        # shouldn't record this
        self.assertEqual(26, getter()(5, b=6, c=7, d=8),
                         'Function didn\'t work after spying')

        self.assertEqual(
            spy.calls, 
            { 
                target.__name__: [ 
                    Call(
                        args=(1, 2), 
                        kwargs={'c': 3, 'd': 4}, 
                        return_value=10
                    )
                ]
            }
        )
