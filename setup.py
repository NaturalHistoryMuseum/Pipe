# !/usr/bin/env python
# encoding: utf-8

from setuptools import find_packages, setup

NAME = 'annette'
DESCRIPTION = ''
URL = 'https://github.com/NaturalHistoryMuseum/annette'
EMAIL = 'data@nhm.ac.uk'
AUTHOR = 'Sarah Vincent, Ginger Butcher'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '0.1'

with open('deploy/requirements.txt', 'r') as req_file:
    REQUIRED = [r.strip() for r in req_file.readlines()]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    entry_points='''
    ''',
    license='GPLv3+',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython'
        ]
    )
