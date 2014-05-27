from decorator import decorate


from .replayers import sequence, pattern_match

SEQUENCE = 'sequence'
PATTERN_MATCH = 'pattern_match'


def get_replayer(spy, attribute, context):
    mode = spy.replay_mode or SEQUENCE

    if spy.replay_mode == PATTERN_MATCH:
        module = pattern_match
    else:
        module = sequence

    decorator_map = {
        'function': module.FunctionReplayer(spy),
        'instance_method': module.InstanceMethodReplayer(spy),
        'class_method': module.ClassMethodReplayer(spy),
        'static_method': module.StaticMethodReplayer(spy)
    }

    return decorate(attribute, context, decorator_map)


class Replayer(object):
    def replay(self, fn, *args, **kwargs):
        raise NotImplementedError
