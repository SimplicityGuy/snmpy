#!/usr/bin/env python

"""Setup configuration."""

from setuptools import setup, find_packages

setup(
    name='snmpy',
    version='1.0.0',
    description='Simple pysnmp wrapper.',
    long_description='The pysnmp library is somewhat tricky to work with. This package makes reading and writing SNMP OIDs much easier.',  # noqa
    url='https://github.com/SimplicityGuy/snmpy',
    author='Robert Wlodarczyk',
    author_email='robert@simplicityguy.com',
    license='Apache License 2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Monitoring',
    ],
    keywords='snmp monitoring',
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    setup_requires=['setuptools-lint', 'flake8', 'sphinx'],
    install_requires=['pysnmp'],
)
