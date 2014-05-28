class Replayer(object):
    def replay(self, fn, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, fn, *args, **kwargs):
        return self.replay(fn, *args, **kwargs)
