# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

PACKAGE = 'pebblebox_election_schemes'
VERSION = '0.1'

setup(
    name=PACKAGE, version=VERSION,
    description="Contains election schemes for pebblebox.",
    packages=[
        'pebblebox_election_schemes',
        'pebblebox_election_schemes.schemes',
        'pebblebox_election_schemes.schemes.majorityjudgement',
        'pebblebox_election_schemes.schemes.singletransferablevote',
    ],
    license='MIT',
    author='/dev/fort 9',
    author_email='contact@devfort.com',
    install_requires=[
    ],
    url='https://github.com/devfort/pebblebox_election_schemes',
    classifiers=[
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
