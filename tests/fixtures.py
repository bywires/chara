def dummy_function(a, b=0, *args, **kwargs):
    return a + b + sum(args) + sum(kwargs.values())


class Dummy(object):
    dummy_attribute = 123

    def dummy_instance_method(self, a, b=0, *args, **kwargs):
        assert isinstance(self, Dummy)
        return dummy_function(a, b=b, *args, **kwargs)

    @classmethod
    def dummy_class_method(cls, a, b=0, *args, **kwargs):
        assert cls is Dummy
        return dummy_function(a, b=b, *args, **kwargs)

    @staticmethod
    def dummy_static_method(a, b=0, *args, **kwargs):
        return dummy_function(a, b=b, *args, **kwargs)


class Value(object):
    def __init__(self):
        self.value = None

    def get(self):
        return self.value


class Cache(object):
    def __init__(self):
        self.values = {}

    def get(self, k):
        return self.values[k]

    def set(self, k, v):
        self.values[k] = v
