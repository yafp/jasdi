# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='jasdi',
    version='0.0.1',
    description='Just a simple directory indexer',
    long_description=readme,
    author='Florian Poeck',
    author_email='fidel@yafp.de',
    url='https://github.com/yafp/jasdi',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
