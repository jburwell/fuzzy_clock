#!/usr/bin/env python

from distutils.core import setup

PACKAGE_NAME="fuzzy_clock"

setup(name=PACKAGE_NAME,
      version='1.0.0',
      description='Library to render time as a fuzzy phrase',
      author='John Burwell',
      author_email='meaux@cockamamy.net',
      url='https://github.com/jburwell/fuzzy_clock',
      license="Apache",
      packages=[PACKAGE_NAME],
     )
