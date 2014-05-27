from decorator import decorator

from .chara import Spy
from . import storage
from .storage import SEQUENCE, PATTERN_MATCH


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
    def wrapper(fn, sequence_mode=True, pattern_match_mode=False, *args, **kwargs):
        spy = Spy(target)

        storage.read(fn, spy)

        if sequence_mode:
            spy.replay_mode(SEQUENCE)

        elif pattern_match_mode:
            spy.replay_mode(PATTERN_MATCH)

        with spy.replay():
            return fn(*args, **kwargs)

    return wrapper


