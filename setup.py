from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='snmpy',
    version='0.1.0',
    description='Simple pysnmp wrapper.',
    long_description=long_description,
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
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
