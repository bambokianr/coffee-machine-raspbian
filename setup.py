#!/usr/bin/env python

import os
from distutils.core import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='GPIOSimulator',
    version='0.1',
    description='Raspberry Pi GPIO simulator',
    long_description=read('README.md'),
    author='Johannes Spielmann',
    author_email='j@spielmannsolutions.com',
    url='https://gitlab.com/shezi/GPIOSimulator',
    packages=['RPiSim',],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
)
