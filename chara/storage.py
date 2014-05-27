import os, pickle, inspect


def write(test_callable, call_list):
    file_info = get_record_file_info(test_callable)

    if not os.path.isdir(file_info['dir']):
        os.makedirs(file_info['dir'])

    with open(file_info['path'], 'w+b') as handle:
        pickle.dump(call_list.calls, handle)


def read(test_callable, call_list):
    file_info = get_record_file_info(test_callable)

    with open(file_info['path'], 'r+b') as handle:
        call_list.calls = pickle.load(handle)


def get_record_file_info(test_callable):
    test_file = inspect.getfile(test_callable)
    path = os.path.dirname(test_file) + '/.chara/'

    if hasattr(test_callable, 'im_class'):
        path += test_callable.im_class + '/'

    return {
        'dir': path,
        'file': test_callable.__name__ + '.pickle',
        'path': path + test_callable.__name__ + '.pickle'
    }
