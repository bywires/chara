from contextlib import contextmanager
from functools import partial

from mock import _get_target

from .exceptions import CharaException, CallNotFoundException
from .patchers import get_patcher
from .recorders import get_recorder
from .replayers import get_replayer


class Spy(object):
    def __init__(self, target):
        self.context_getter, self.name = _get_target(target)
        self.patcher = None
        self.calls = {}
        self.replay_mode = None

    def start_recording(self):
        self._start(get_recorder)

    def stop_recording(self):
        self._stop()

    def start_replaying(self):
        self._start(get_replayer)

    def stop_replaying(self):
        self._stop()

    @contextmanager
    def record(self):
        self.start_recording()
        yield
        self.stop_recording()

    @contextmanager
    def replay(self):
        self.start_replaying()
        yield
        self.stop_replaying()

    def add_call(self, fn, args, kwargs, return_value):
        self.calls.setdefault(fn.__name__, []).append(Call(
            args,
            kwargs,
            return_value
        ))

    def get_call(self, fn, index):
        try:
            return self.calls[fn.__name__][index]
        except IndexError:
            raise CallNotFoundException()

    def _start(self, decorator_factory):
        self.patcher = get_patcher(
            # replayer factory
            partial(decorator_factory, self),

            self.name,

            # import the context
            self.context_getter(),
        )

        self.patcher.start()

    def _stop(self):
        if not self.patcher:
            raise CharaException('Spy cannot be stopped because it was '
                                 'not started')

        self.patcher.stop()

        self.patcher = None


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
