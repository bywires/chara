from .exceptions import PatcherCreationException
from .watchers import get_watcher, is_watchable
from .detectors import is_static_method, is_callable, is_class, get_callables


def get_patcher(spy, name, context):
    attribute = getattr(context, name)

    if is_class(attribute):
        # In this case the attribute is actually the context.
        context = attribute

        # Get all the callables on the object and get patchers for them.
        return MultiPatcher([
            get_patcher(spy, name, context) \
            for name, attribute in get_callables(context).items() \
            if is_watchable(attribute, context)
        ])

    elif is_callable(attribute):
        watcher = get_watcher(spy, attribute, context)

        if is_static_method(attribute, context):
            return StaticMethodPatcher(name, attribute, context, watcher)

        else:
            return CallablePatcher(name, attribute, context, watcher)

    else:
        raise PatcherCreationException(
            'Cannot patch {name} ({attribute}) of {context}'.format(
                name=name,
                attribute=attribute,
                context=context
            )
        )


class Patcher(object):
    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


class CallablePatcher(Patcher):
    def __init__(self, name, attribute, context, watcher):
        self.name = name
        self.attribute = attribute
        self.context = context
        self.watcher = watcher

    def start(self):
        setattr(self.context, self.name, self.watcher)

    def stop(self):
        setattr(self.context, self.name, self.attribute)
    

class StaticMethodPatcher(CallablePatcher):
    def stop(self):
        setattr(self.context, self.name, staticmethod(self.attribute))

        
class MultiPatcher(Patcher):
    def __init__(self, patchers):
        self.patchers = patchers

    def start(self):
        for p in self.patchers: p.start()

    def stop(self):
        for p in self.patchers: p.stop()
