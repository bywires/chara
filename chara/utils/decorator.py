from __future__ import absolute_import

from decorator import decorator


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
