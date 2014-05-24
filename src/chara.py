import types
from contextlib import contextmanager
from decorator import decorator

from mock import _get_target


class Spy(object):
    def __init__(self, target):
        self.target_getter, self.attribute_name = _get_target(target)
        self.calls = []

    def start(self):
        # import the target
        self.target = self.target_getter()
        self.old_attribute = getattr(self.target, self.attribute_name)

        # replace attribute
        setattr(self.target, self.attribute_name, 
                decorate(self.old_attribute, self))

    def stop(self):
        if not self.target:
            raise Exception('Spy cannot be stopped because it was not started')

        # restore attribute
        setattr(self.target, self.attribute_name, self.old_attribute)

    @contextmanager
    def record(self):
        self.start()
        yield
        self.stop()


def decorate(o, spy):
    t = type(o)

    if t is types.FunctionType:
        return decorator(watch_function(spy), o)
    if t is types.MethodType:
        return decorator(watch_method(spy), o.im_func)
    elif t is types.ObjectType:
        pass
    else:
        raise Exception('Cannot spy on type {}'.format(t))


def watch_function(spy):
    def wrapper(fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        spy.calls.append(Call(
            args, 
            kwargs, 
            return_value
        ))

        return return_value

    return wrapper

def watch_method(spy):
    def wrapper(fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        spy.calls.append(Call(
            args[1:], # discard 'self'
            kwargs, 
            return_value
        ))

        return return_value

    return wrapper

    
class Call(object):
    def __init__(self, args, kwargs, return_value):
        self.args = args
        self.kwargs = kwargs
        self.return_value = return_value

    def __eq__(self, other): 
        return self.__dict__ == other.__dict__
