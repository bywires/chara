import types

from decorator import decorator

from .exceptions import CharaException


def get_watcher(spy, o):
    t = type(o)

    if t is types.FunctionType:
        return watch_function(spy, o)

    if t is types.MethodType:
        if o.__self__ is not None:
            return watch_class_method(spy, o)
        else:
            return watch_instance_method(spy, o)

    elif t is types.ObjectType:
        pass

    else:
        raise CharaException('Cannot spy on type {}'.format(t))


def watch_function(spy, o):
    def wrapper(fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        spy.add_call(
            args, 
            kwargs, 
            return_value
        )

        return return_value

    return decorator(wrapper, o)


def watch_instance_method(spy, o):
    def wrapper(fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        spy.add_call(
            args[1:], # discard 'self'
            kwargs, 
            return_value
        )

        return return_value

    return decorator(wrapper, o.im_func)


def watch_class_method(spy, o):
    def wrapper(fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        spy.add_call(
            args[1:], # discard 'cls'
            kwargs, 
            return_value
        )

        return return_value

    return classmethod(decorator(wrapper, o.__get__(o.__self__).im_func))
