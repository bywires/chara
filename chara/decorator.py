from __future__ import absolute_import

from decorator import decorator

from .exceptions import DecoratorException
from .detectors import is_static_method, is_function, is_class_method, \
    is_instance_method


def decorate(attribute, context, decorator_map):
    if is_static_method(attribute, context):
        return static_method(decorator_map['static_method'], attribute)

    elif is_function(attribute):
        return function(decorator_map['function'], attribute)

    elif is_class_method(attribute):
        return class_method(decorator_map['class_method'], attribute)

    elif is_instance_method(attribute):
        return instance_method(decorator_map['instance_method'], attribute)

    else:
        raise DecoratorException(
            'Cannot decorate {attribute} of {context}'.format(
                attribute=attribute,
                context=context
            )
        )


def is_decorable(attribute, context):
    return is_static_method(attribute, context) or \
        is_function(attribute) or \
        is_class_method(attribute) or \
        is_instance_method(attribute)


def function(outer, inner):
    return decorator(outer, inner)


def instance_method(outer, inner):
    return decorator(outer, inner.im_func)


def class_method(outer, inner):
    return classmethod(decorator(
        outer,
        inner.__get__(inner.__self__).im_func
    ))


def static_method(outer, inner):
    return staticmethod(decorator(outer, inner))
