# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

PACKAGE = 'turnout_election_schemes'
VERSION = '0.3'

setup(
    name=PACKAGE, version=VERSION,
    description="Library implementing (some) modern election schemes.",
    packages=[
        'turnout_election_schemes',
        'turnout_election_schemes.schemes',
        'turnout_election_schemes.schemes.majorityjudgement',
        'turnout_election_schemes.schemes.singletransferablevote',
    ],
    scripts=[
      'scripts/run_an_election',
    ],
    license='MIT',
    author='/dev/fort 9',
    author_email='turnout-elections@groups.google.com',
    install_requires=[
    ],
    url='https://github.com/devfort/turnout-election-schemes',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
    ],
)
