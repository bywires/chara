from .exceptions import PatcherCreationException
from .decorator import is_decorable
from .detectors import is_static_method, is_callable, is_class, get_callables


def get_patcher(decorator_factory, name, context):
    attribute = getattr(context, name)

    if is_class(attribute):
        # In this case the attribute is actually the context.
        context = attribute

        # Get all the callables on the object and get patchers for them.
        return MultiPatcher([
            get_patcher(decorator_factory, name, context) \
            for name, attribute in get_callables(context).items() \
            if is_decorable(attribute, context)
        ])

    elif is_callable(attribute):
        decorator = decorator_factory(attribute, context)

        if is_static_method(attribute, context):
            return StaticMethodPatcher(name, attribute, context, decorator)

        else:
            return CallablePatcher(name, attribute, context, decorator)

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
    def __init__(self, name, attribute, context, decorator):
        self.name = name
        self.attribute = attribute
        self.context = context
        self.decorator = decorator

    def start(self):
        setattr(self.context, self.name, self.decorator)

    def stop(self):
        setattr(self.context, self.name, self.attribute)


class StaticMethodPatcher(CallablePatcher):
    def stop(self):
        setattr(self.context, self.name, staticmethod(self.attribute))


class MultiPatcher(Patcher):
    def __init__(self, patchers):
        self.patchers = patchers

    def start(self):
        for patcher in self.patchers:
            patcher.start()

    def stop(self):
        for patcher in self.patchers:
            patcher.stop()
