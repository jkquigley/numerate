#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='numerate',
    version='0.0.0',
    packages=[
        'numerate',
        'numerate.schemes',
    ],
    install_requires=[
        'setuptools',
        'numpy',
        'scipy',
        'matplotlib',
    ],
    maintainer='J. Keane Quigley',
    maintainer_email='s1929908@ed.ac.uk',
    description='Numerical solvers for the advection equation.',
    license='MIT',
    python_requires=">=3.8",
)
