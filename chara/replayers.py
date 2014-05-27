from decorator import decorate


def get_replayer(spy, attribute, context):
    decorator_map = {
        'function': FunctionReplayer(spy),
        'instance_method': InstanceMethodReplayer(spy),
        'class_method': ClassMethodReplayer(spy),
        'static_method': StaticMethodReplayer(spy)
    }

    return decorate(attribute, context, decorator_map)


class Replayer(object):
    def __init__(self, spy):
        self.spy = spy
        self.index = 0

    def replay(self, fn, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, fn, *args, **kwargs):
        return self.replay(fn, *args, **kwargs)
    

class FunctionReplayer(Replayer):
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
