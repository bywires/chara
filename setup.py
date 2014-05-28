#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

requires = [
    'nose',
    'mock',
    'decorator'
]

classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(
    name='chara',
    version='0.0.1',
    description='Chara enables developers to quickly create characterization tests.  Start by creating integration tests using whatever testing framework you prefer.  Using Chara you decorate those test functions to record interactions with specific dependencies.  Afterwards, you can replay the recording and those dependencies will behave as recorded.',
    long_description=readme,
    packages=find_packages(),
    install_requires=requires,
    author='Bob McKee',
    author_email='bmckee@bywires.com',
    url='https://github.com/bywires/chara',
    license='MIT',
    classifiers=classifiers,
)
