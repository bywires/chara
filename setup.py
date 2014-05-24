#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import chara


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as f:
    readme = f.read()

packages = [
    'chara',
]

package_data = {
}

requires = [
    'nose',
    'mock',
    'decroator'
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
    version=chara.__version__,
    description='Tools that recording calls to functions during code execution so those behaviors can be replayed in characterization tests.',
    long_description=readme,
    packages=packages,
    package_data=package_data,
    install_requires=requires,
    author=chara.__author__,
    author_email='bmckee@bywires.com',
    url='https://github.com/bywires/chara',
    license='MIT',
    classifiers=classifiers,
)
