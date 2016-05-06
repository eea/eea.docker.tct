#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup

VERSION = '0.0.1'

setup(
    name='nbsap',
    version=VERSION,
    description='NBSAP',
    author='Cornel Nițu',
    author_email='cornel.nitu@eaudeweb.ro',

    #packages=['app',],
    package_dir={ '' : 'src' },

    install_requires=[
        'django == 1.9.5',
        'mysql-python == 1.2.5',
    ]
)
