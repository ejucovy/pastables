from setuptools import setup, find_packages
import sys, os

version = '0.0'

setup(name='pastables',
      version=version,
      description="Assorted building blocks for WSGI applications using paste and webob",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Ethan Jucovy',
      author_email='ethan.jucovy@gmail.com',
      url='http://github.com/ejucovy/pastables',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'PasteDeploy',
          "WebOb",
      ],
      entry_points="""
[paste.composite_factory]
domain = pastables.domain:composite_factory

[paste.app_factory]
file = pastables.file:app_factory
      """,
      )
