#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages

setup(
    name='cedro',
    version='1.0.2',
    description='Python Cedro Web Feeder API Client',
    author='Paula Grangeiro',
    author_email='contato@paulagrangeiro.com.br',
    url='https://github.com/pgrangeiro/python-cedro-client',
    license='GNU 3',
    python_requires='>=3.6',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['requests>=2.18'],
)
