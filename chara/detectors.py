import inspect, types


def is_class(o):
    return inspect.isclass(o)


def is_function(o):
    return inspect.isfunction(o)


def is_class_method(o):
    return inspect.ismethod(o) and o.__self__ is not None


def is_instance_method(o):
    return inspect.ismethod(o) and o.__self__ is None
    

def is_static_method(o, context=None):
    return inspect.isfunction(o) and inspect.isclass(context)


def is_callable(o):
    return callable(o)


def get_callables(o):
    return { k: getattr(o, k) for k in dir(o) \
             if callable(getattr(o, k)) }
