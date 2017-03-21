#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Install contain."""

from setuptools import find_packages
from setuptools import setup

setup(
    name='contain',
    author='Za Wilgustus',
    author_email='zancas@contains.io',
    license='MIT',
    url='https://github.com/contains-io/contain.git',
    use_scm_version=True,
    packages=find_packages(exclude=['tests', 'docs']),
    install_requires=['docker-py >= 1.10.6, < 1.11',
                      'jinja2 >= 2.8, < 3',
                      'rcli >= 0.2.5, < 1'],
    setup_requires=['pytest-runner',
                    'rcli >= 0.2.5, < 1',
                    'setuptools_scm'],
    tests_require=['pytest'],
    autodetect_commands=True
)
