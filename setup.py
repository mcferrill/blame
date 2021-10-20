#!/usr/bin/env python

from distutils.core import setup


setup(name='Blame',
      version='1.0',
      packages=['blame'],
      entry_points={
          'console_scripts': [
              'blame=blame.blame:main',
          ]
      },
      install_requires=['docopt', 'pygments', 'termcolor'])
