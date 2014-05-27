import os, pickle, inspect


def dump(test_callable, spy):
    file_info = get_record_file_info(test_callable)
    file_path = file_info['path'] + file_info['file']

    if not os.path.isdir(file_info['path']):
        os.makedirs(file_info['path'])

    with open(file_path, 'w+b') as handle:
        pickle.dump(spy.calls, handle)


def load(test_callable):
    pass


def get_record_file_info(test_callable):
    test_file = inspect.getfile(test_callable)
    path = os.path.dirname(test_file) + '/.chara/'

    if hasattr(test_callable, 'im_class'):
        path += test_callable.im_class + '/'

    return {
        'path': path,
        'file': test_callable.__name__ + '.pickle'
    }
