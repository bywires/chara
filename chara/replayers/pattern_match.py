from .interface import Replayer
from ..exceptions import CallNotFoundException


class PatternMatchReplayer(Replayer):
    def __init__(self, spy):
        self.spy = spy
        self.index = None

    def get_key(self, args, kwargs):
        raise NotImplementedError

    def replay(self, fn, *args, **kwargs):
        if self.index is None:
            self.index = self.build_index(fn)

        key = self.get_key(args, kwargs)

        if key in self.index:
            return self.index[key]
        else:
            raise CallNotFoundException()

    def build_index(self, fn):
        return {get_key(call.args, call.kwargs): call.return_value \
                for call in self.spy.calls.get(fn.__name__, [])}


class FunctionReplayer(PatternMatchReplayer):
    def get_key(self, args, kwargs):
        return get_key(args, kwargs)


class InstanceMethodReplayer(PatternMatchReplayer):
    def get_key(self, args, kwargs):
        return get_key(args[1:], kwargs)


class ClassMethodReplayer(InstanceMethodReplayer):
    pass


class StaticMethodReplayer(FunctionReplayer):
    pass


def get_key(args, kwargs):
    return (
        args,
        tuple(sorted(kwargs.items()))
    )
