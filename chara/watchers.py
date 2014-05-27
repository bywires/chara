from decorator import decorate


def get_watcher(spy, attribute, context):
    decorator_map = {
        'function': FunctionWatcher(spy),
        'instance_method': InstanceMethodWatcher(spy),
        'class_method': ClassMethodWatcher(spy),
        'static_method': StaticMethodWatcher(spy)
    }

    return decorate(attribute, context, decorator_map)


class Watcher(object):
    def __init__(self, spy):
        self.spy = spy

    def watch(self, fn, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, fn, *args, **kwargs):
        return self.watch(fn, *args, **kwargs)
    

class FunctionWatcher(Watcher):
    def watch(self, fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        self.spy.add_call(
            args, 
            kwargs, 
            return_value
        )

        return return_value


class InstanceMethodWatcher(Watcher):
    def watch(self, fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        self.spy.add_call(
            args[1:], # discard 'self'
            kwargs, 
            return_value
        )

        return return_value


class ClassMethodWatcher(InstanceMethodWatcher):
    pass


class StaticMethodWatcher(FunctionWatcher):
    pass
