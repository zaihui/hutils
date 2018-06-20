# -*- coding: utf-8 -*-
import pypandoc
from setuptools import setup

import hutils

setup(
    name='hutils',
    version=hutils.__version__,
    description='a charming python web util-library',
    long_description=pypandoc.convert('README.md', 'rst'),
    author='ZaiHui Dev',
    author_email='llk@kezaihui.com',
    url='https://github.com/zaihui/hutils/',
    license='MIT License',
    install_requires=open('requirements.txt').readlines(),
    packages=['hutils'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
