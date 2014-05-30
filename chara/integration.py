from decorator import decorator

from .chara import Spy
from . import storage
from .replayers import SEQUENCE, PATTERN_MATCH


def record(target):
    @decorator
    def wrapper(fn, *args, **kwargs):
        spy = Spy(target)

        with spy.record():
            result = fn(*args, **kwargs)

        storage.write(fn, spy, args[0] if args else None)

        return result

    return wrapper


def replay(target, sequence_mode=False, pattern_match_mode=False):
    @decorator
    def wrapper(fn, *args, **kwargs):
        spy = Spy(target)

        storage.read(fn, spy, args[0] if args else None)

        if sequence_mode:
            spy.replay_mode = SEQUENCE

        elif pattern_match_mode:
            spy.replay_mode = PATTERN_MATCH

        with spy.replay():
            return fn(*args, **kwargs)

    return wrapper


