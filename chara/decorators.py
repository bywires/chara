from decorator import decorator

from .chara import Spy
from . import records


def record(target):
    @decorator
    def wrapper(fn, *args, **kwargs):
        spy = Spy(target)
    
        with spy.record():
            result = fn(*args, **kwargs)

        records.dump(fn, spy)
        
        return result

    return wrapper


def replay(target):
    @decorator
    def wrapper(fn, *args, **kwargs):
        return fn(*args, **kwargs)

    return wrapper


