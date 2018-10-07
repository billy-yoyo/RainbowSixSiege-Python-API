# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import re, os

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

version = '0.8.0'

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(name='r6sapi',
      author='billyoyo',
      url='https://github.com/billy-yoyo/RainbowSixSiege-Python-API',
      version=version,
      packages=find_packages(),
      license='MIT',
      description='Interface for Ubisoft API',
      long_description=readme,
      include_package_data=True,
      install_requires=requirements,
      extras_require={},
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
      ]
)