class CharaException(Exception):
    pass


class DecoratorException(CharaException):
    pass


class PatcherCreationException(CharaException):
    pass


class CallNotFoundException(CharaException):
    pass
