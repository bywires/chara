#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as f:
    readme = f.read()

install_requires = [
    'mock',
    'decorator'
]

tests_require = [
    'nose'
]

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

keywords = [
    'record',
    'replay',
    'spy',
    'test',
]

version = '0.1.5'

setup(
    name='chara',
    version=version,
    description='Chara enables developers to quickly create characterization tests.  Start by creating integration tests using whatever testing framework you prefer.  Using Chara you decorate those test functions to record interactions with specific dependencies.  Afterwards, you can replay the recording and those dependencies will behave as recorded.',
    long_description=readme,
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    test_suite = 'nose.collector',
    author='Bob McKee',
    author_email='bmckee@bywires.com',
    url='https://github.com/bywires/chara',
    download_url='https://github.com/bywires/chara/tarball/' + version,
    license='MIT',
    classifiers=classifiers,
    keywords=keywords
)
