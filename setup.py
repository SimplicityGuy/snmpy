from setuptools import setup, find_packages

setup(
    name='snmpy',
    version='0.1.0.2',
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
    packages=find_packages(exclude=['contrib', 'docs', 'test*']),
    install_requires=['pysnmp'],
    platforms='any',
)
