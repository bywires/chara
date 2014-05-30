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


def is_slot_wrapper(obj, context):
    return callable(obj) and inspect.isclass(context) and \
        hasattr(obj, '__objclass__')


def is_callable(obj):
    return callable(obj)


def is_function_in_class(obj):
    """ When decorating a instance, class, or static method declaration the
    callable is not yet bound so it appears as just a function.  This allows
    us to speculate whether or not the callable is a class member """

    if not is_function(obj):
        return False

    arg_spec = inspect.getargspec(obj)

    if len(arg_spec.args) < 1:
        return False

    if arg_spec.args[0] == 'self':
        return True

    return False


def get_callables(obj):
    return {k: getattr(obj, k) for k in dir(obj)
            if callable(getattr(obj, k))}
