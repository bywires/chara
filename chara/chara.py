from contextlib import contextmanager

from mock import _get_target

from .watchers import get_watcher
from .exceptions import CharaException
from .detect import is_static_method

class Spy(object):
    def __init__(self, target):
        self.target_getter, self.attribute_name = _get_target(target)
        self.calls = []

    def start(self):
        # import the target
        self.target = self.target_getter()

        # store old attribute to be restored later
        self.old_attribute = getattr(self.target, self.attribute_name)

        # replace attribute
        setattr(self.target, self.attribute_name, 
                get_watcher(self, self.target, self.old_attribute))

    def stop(self):
        if not self.target:
           raise CharaException('Spy cannot be stopped because it was '
                                'not started')

        # restore attribute
        if is_static_method(self.old_attribute, context=self.target):
            setattr(self.target, self.attribute_name, 
                    staticmethod(self.old_attribute))
        else:
            setattr(self.target, self.attribute_name, self.old_attribute)

    @contextmanager
    def record(self):
        self.start()
        yield
        self.stop()

    def add_call(self, args, kwargs, return_value):
        self.calls.append(Call(
            args,
            kwargs, 
            return_value
        ))

    
class Call(object):
    def __init__(self, args, kwargs, return_value):
        self.args = args
        self.kwargs = kwargs
        self.return_value = return_value

    def __str__(self):
        return super(Call, self).__str__() + ' ' + str(self.__dict__)

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

    def __ne__(self, other): 
        return not self.__eq__(other)
