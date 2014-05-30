import inspect


def is_class(obj):
    return inspect.isclass(obj)


def is_function(obj):
    return inspect.isfunction(obj)


def is_class_method(obj):
    return inspect.ismethod(obj) and obj.__self__ is not None


def is_instance_method(obj):
    return inspect.ismethod(obj) and obj.__self__ is None


def is_static_method(obj, context):
    return inspect.isfunction(obj) and inspect.isclass(context)


def is_slobjt_wrapper(obj, context):
    return callable(obj) and inspect.isclass(context) and \
        hasattr(obj, '__objclass__')


def is_callable(obj):
    return callable(obj)


def get_callables(obj):
    return {k: getattr(obj, k) for k in dir(obj)
            if callable(getattr(obj, k))}
