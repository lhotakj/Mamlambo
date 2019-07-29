#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import Mamlambo
import os

# Package meta-data.
NAME = Mamlambo.__name__
DESCRIPTION = 'Simple Python WSGI web-framework inpired by .NET winforms'
URL = 'https://github.com/lhotakj/Mamlambo'
AUTHOR_EMAIL = 'jarda@lhotak.net'
AUTHOR = 'Jaroslav Lhoták'
REQUIRES_PYTHON = '>=3.4'
VERSION = Mamlambo.__version__
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3 :: Only',
    'Topic :: Internet',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content']

KEYWORDS = ['python3', 'web framework', 'fast', 'wsgi', 'apache', 'master page', 'template', 'kajiki']


# read long description
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as file_description:
    long_description = file_description.read()

# read dev requirements
file_requirements = os.path.join(os.path.dirname(__file__), 'requirements.txt')
with open(file_requirements) as f:
    list_requirements = [l.strip() for l in f.readlines()]

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=long_description,
      long_description_content_type='text/markdown',
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=list_requirements,
      license='MIT',
      packages=find_packages('Mamlambo'),
      zip_safe=False,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS
      )