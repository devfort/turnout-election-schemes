# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

PACKAGE = 'turnout_election_schemes'
VERSION = '0.2'

setup(
    name=PACKAGE, version=VERSION,
    description="Contains election schemes for pebblebox.",
    packages=[
        'turnout_election_schemes',
        'turnout_election_schemes.schemes',
        'turnout_election_schemes.schemes.majorityjudgement',
        'turnout_election_schemes.schemes.singletransferablevote',
    ],
    license='MIT',
    author='/dev/fort 9',
    author_email='contact@pebblebox.org',
    install_requires=[
    ],
    url='https://github.com/devfort/turnout_election_schemes',
    classifiers=[
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
