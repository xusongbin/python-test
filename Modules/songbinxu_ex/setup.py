#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='myDriver',
    version='1.0.0',
    author='xusongbin',
    author_email='zasongbinxu@163.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'xlwt', 'xlrd', 'pyserial',
    ],
)