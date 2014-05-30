from decorator import decorate


def get_recorder(spy, attribute, context):
    decorator_map = {
        'function': FunctionRecorder(spy),
        'instance_method': InstanceMethodRecorder(spy),
        'class_method': ClassMethodRecorder(spy),
        'static_method': StaticMethodRecorder(spy)
    }

    return decorate(attribute, context, decorator_map)


class Recorder(object):
    def __init__(self, spy):
        self.spy = spy

    def record(self, fn, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, fn, *args, **kwargs):
        return self.record(fn, *args, **kwargs)


class FunctionRecorder(Recorder):
    def record(self, fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        self.spy.add_call(
            fn,
            args,
            kwargs,
            return_value
        )

        return return_value


class InstanceMethodRecorder(Recorder):
    def record(self, fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        self.spy.add_call(
            fn,
            args[1:], # discard 'self'
            kwargs,
            return_value
        )

        return return_value


class ClassMethodRecorder(InstanceMethodRecorder):
    pass


class StaticMethodRecorder(FunctionRecorder):
    pass
