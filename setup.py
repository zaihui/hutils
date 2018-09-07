# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

import hutils

with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name='hutils',
    version=hutils.__version__,
    description='a charming python web util-library',
    long_description=description,
    long_description_content_type='text/markdown',
    author='ZaiHui Dev',
    author_email='llk@kezaihui.com',
    url='https://github.com/zaihui/hutils/',
    license='MIT License',
    install_requires=open('requirements.txt').readlines(),
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
