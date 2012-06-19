# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='imagy',
    version='0.0.1',
    description='automatically optimize images',
    long_description=readme,
    author='Dominik Dabrowski',
    author_email='dominik@silberrock.com',
    url='https://github.com/doda/imagy',
    license=license,
    packages=find_packages(),
    entry_points={
        "console_scripts": ['imagy=imagy.cl:main']
        },
)

