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
