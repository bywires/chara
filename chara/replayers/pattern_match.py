from . import Replayer


class FunctionReplayer(Replayer):
    def __init__(self, spy):
        self.spy = spy

        # TODO - implement pattern matching

    def replay(self, fn, *args, **kwargs):
        return_value = self.spy.get_call(fn, self.index).return_value
        self.index += 1
        return return_value


class InstanceMethodReplayer(FunctionReplayer):
    pass


class ClassMethodReplayer(InstanceMethodReplayer):
    pass


class StaticMethodReplayer(FunctionReplayer):
    pass
