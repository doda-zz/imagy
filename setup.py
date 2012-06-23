# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='imagy',
    version='0.2.2',
    description='A daemon to automatically handle image optimization',
    author='Dominik Dabrowski',
    author_email='dominik@silberrock.com',
    url='https://github.com/doda/imagy',
    license=open('LICENSE').read(),
    long_description=open('README.rst').read(),
    packages=find_packages(),
    package_data={'': ['README.rst','LICENSE']},
    install_requires=['watchdog','path.py'],
    entry_points={
        "console_scripts": ['imagy=imagy.cl:main']
        },
)

