from .exceptions import CharaException
from .watchers import get_watcher
from .detect import is_static_method, is_callable, is_class


def get_patcher(spy, name, context):
    attribute = getattr(context, name)
    watcher = get_watcher(spy, attribute, context)

    if is_static_method(attribute, context):
        patcher = StaticMethodPatcher

    elif is_callable(attribute):
        patcher = CallablePatcher

    elif is_class(attribute):
        pass

    else:
        raise CharaException('Cannot patch {name} ({attribute}) '
                             'of {context}'.format(
                                 name=name,
                                 attribute=attribute,
                                 context=context
                             ))

    return patcher(name, attribute, context, watcher)


class Patcher(object):
    def __init__(self, name, attribute, context, watcher):
        self.name = name
        self.attribute = attribute
        self.context = context
        self.watcher = watcher

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError


class CallablePatcher(Patcher):
    def start(self):
        setattr(self.context, self.name, self.watcher)

    def stop(self):
        setattr(self.context, self.name, self.attribute)
    

class StaticMethodPatcher(CallablePatcher):
    def stop(self):
        setattr(self.context, self.name, staticmethod(self.attribute))
        
