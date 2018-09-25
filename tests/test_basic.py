#!/usr/bin/env python
"""test script for jasdi."""

# ------------------------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------------------------
from .context import jasdi

import unittest

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True


if __name__ == '__main__':
unittest.main()
