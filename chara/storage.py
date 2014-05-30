import os, pickle, inspect

from .detectors import is_function_in_class


def write(test_callable, spy, first_arg=None):
    file_info = get_record_file_info(test_callable, first_arg)

    if not os.path.isdir(file_info['dir']):
        os.makedirs(file_info['dir'])

    with open(file_info['path'], 'w+b') as handle:
        pickle.dump(spy.calls, handle)


def read(test_callable, spy, first_arg=None):
    file_info = get_record_file_info(test_callable, first_arg)

    with open(file_info['path'], 'r+b') as handle:
        spy.calls = pickle.load(handle)


def delete(test_callable, first_arg=None):
    file_info = get_record_file_info(test_callable, first_arg)

    if os.path.isfile(file_info['path']):
        os.unlink(file_info['path'])


def get_record_file_info(test_callable, first_arg=None):
    test_file = inspect.getfile(test_callable)
    path = os.path.dirname(test_file) + '/.chara/' + \
           os.path.splitext(os.path.basename(test_file))[0] + '/'
    file_name =  test_callable.__name__ + '.pickle'

    if is_function_in_class(test_callable) and first_arg:
        path += first_arg.__class__.__name__ + '/'

    return {
        'dir': path,
        'file': file_name,
        'path': path + file_name
    }
