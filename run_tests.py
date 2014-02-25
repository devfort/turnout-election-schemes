#!/usr/bin/env python

import unittest
import sys

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('tests')

    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
