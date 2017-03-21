#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Install contain."""

from setuptools import find_packages
from setuptools import setup

import contain

setup(
    name='contain',
    version=contain.__version__,
    author='Za Wilgustus',
    author_email='zancas@contains.io',
    license='MIT',
    url='https://github.com/contains-io/contain.git',
    packages=find_packages(),
    install_requires=['docker-py >= 1.10.6, < 1.11',
                      'jinja2 >= 2.8, < 3',
                      'rcli >= 0.1.2, < 1'],
    setup_requires=['pytest-runner', 'rcli >= 0.1.2, < 1'],
    tests_require=['pytest'],
    autodetect_commands=True,
    entry_points={'pytest11': ['contain_fixtures = contain_plugins.fixtures']}
)
