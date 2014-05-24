from contextlib import contextmanager

from mock import _get_target

from .exceptions import CharaException
from .patchers import get_patcher


class Spy(object):
    def __init__(self, target):
        self.context_getter, self.name = _get_target(target)
        self.calls = []

    def start(self):
        self.patcher = get_patcher(
            self, 
            self.name, 
            self.context_getter() # import the context
        )

        self.patcher.start()

    def stop(self):
        if not self.patcher:
           raise CharaException('Spy cannot be stopped because it was '
                                'not started')

        self.patcher.stop()

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
