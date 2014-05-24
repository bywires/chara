from decorator import decorator

from .exceptions import CharaException
from .detectors import is_static_method, is_function, is_class_method, \
    is_instance_method, is_class, get_callables


def get_watcher(spy, attribute, context):
    t = type(attribute)

    if is_static_method(attribute, context):
        return watch_static_method(spy, attribute)

    elif is_function(attribute):
        return watch_function(spy, attribute)

    elif is_class_method(attribute):
        return watch_class_method(spy, attribute)

    elif is_instance_method(attribute):
        return watch_instance_method(spy, attribute)

    elif is_class(attribute):
        pass

    else:
        raise CharaException('Cannot spy on {attribute} '
                             'of {context}'.format(
                                 attribute=attribute,
                                 context=context
                             ))


def watch_function(spy, attribute):
    def wrapper(fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        spy.add_call(
            args, 
            kwargs, 
            return_value
        )

        return return_value

    return decorator(wrapper, attribute)


def watch_instance_method(spy, attribute):
    def wrapper(fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        spy.add_call(
            args[1:], # discard 'self'
            kwargs, 
            return_value
        )

        return return_value

    return decorator(wrapper, attribute.im_func)


def watch_class_method(spy, attribute):
    def wrapper(fn, *args, **kwargs):
        return_value = fn(*args, **kwargs)

        spy.add_call(
            args[1:], # discard 'cls'
            kwargs, 
            return_value
        )

        return return_value

    bound_fn = attribute.__get__(attribute.__self__).im_func

    return classmethod(decorator(wrapper, bound_fn))


def watch_static_method(spy, attribute):
    return staticmethod(watch_function(spy, attribute))
