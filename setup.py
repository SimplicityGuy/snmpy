from setuptools import setup
from codecs import open
from os import path
from re import compile
from ast import literal_eval

here = path.abspath(path.dirname(__file__))
_version_re = compile(r'__version__\s+=\s+(.*)')

with open('snmpy/__init__.py', 'rb') as f:
    version = str(literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='snmpy',
    version=version,
    description='Simple pysnmp wrapper.',
    long_description='The pysnmp library is somewhat tricky to work with. This package makes reading and writing SNMP OIDs much easier.',
    url='https://github.com/SimplicityGuy/snmpy',
    author='Robert Wlodarczyk',
    author_email='robert@simplicityguy.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Monitoring',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='snmp monitoring',
    install_requires=['pysnmp'],
    platforms='any',
)
