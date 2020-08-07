# !/usr/bin/env python

from distutils.core import setup

setup(name='highlight_mentions',
      version='0.08',
      packages=['highlight_mentions'],
      install_requires=[
          "faker",
          "absl-py",
      ],
      package_dir={'highlight_mentions': 'highlight_mentions'}
      )