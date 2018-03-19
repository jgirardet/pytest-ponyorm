#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-ponyorm',
    version='0.2.3',
    author='Jimmy Girardet',
    author_email='ijkl@netc.fr',
    maintainer='Jimmy Girardet',
    maintainer_email='ijkl@netc.fr',
    license='GNU GPL v3.0',
    url='https://github.com/jgirardet/pytest-ponyorm',
    description='PonyORM in Pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_ponyorm'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=3.1.1'],
    classifiers=[
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
    entry_points={
        'pytest11': [
            'ponyorm = pytest_ponyorm',
        ],
    },
)
