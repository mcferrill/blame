#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    print('Setuptools not found!')
    raise SystemExit


setup(name='Blame',
      version='1.0',
      packages=['blame'],
      entry_points={
          'console_scripts': [
              'blame = blame.blame:main',
          ]
      },
      install_requires=['docopt', 'pygments', 'termcolor'])
