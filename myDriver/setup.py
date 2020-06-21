#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='myDriver',
    version='1.0.0',
    author='xusongbin',
    author_email='zasongbinxu@163.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'xlwt', 'xlrd', 'pyserial', 'pycryptodomex', 'requests',
    ],
    url='None',
)

# python setup.py bdist_wheel
# pip install -U dist\
# pip3 install -e .

# python setup.py install
