from decorator import decorator

from .chara import Spy
from . import storage


def record(target):
    @decorator
    def wrapper(fn, *args, **kwargs):
        spy = Spy(target)
    
        with spy.record():
            result = fn(*args, **kwargs)

        storage.write(fn, spy)
        
        return result

    return wrapper


def replay(target):
    @decorator
    def wrapper(fn, *args, **kwargs):
        spy = Spy(target)

        storage.read(fn, spy)

        with spy.replay():
            return fn(*args, **kwargs)

    return wrapper


