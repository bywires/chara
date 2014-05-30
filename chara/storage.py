import os, pickle, inspect


def write(test_callable, spy):
    file_info = get_record_file_info(test_callable)

    if not os.path.isdir(file_info['dir']):
        os.makedirs(file_info['dir'])

    with open(file_info['path'], 'w+b') as handle:
        pickle.dump(spy.calls, handle)


def read(test_callable, spy):
    file_info = get_record_file_info(test_callable)

    with open(file_info['path'], 'r+b') as handle:
        spy.calls = pickle.load(handle)


def delete(test_callable):
    file_info = get_record_file_info(test_callable)

    if os.path.isfile(file_info['path']):
        os.unlink(file_info['path'])

def get_record_file_info(test_callable):
    test_file = inspect.getfile(test_callable)
    path = os.path.dirname(test_file) + '/.chara/'
    file_name = os.path.basename(test_file) + '.' \
                + test_callable.__name__ + '.pickle'

    if hasattr(test_callable, 'im_class'):
        path += test_callable.im_class + '/'

    return {
        'dir': path,
        'file': file_name,
        'path': path + file_name
    }



