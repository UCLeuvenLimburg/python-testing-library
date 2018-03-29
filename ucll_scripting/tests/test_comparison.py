from ucll_scripting.testing import *
import unittest


class ComparisonTests(unittest.TestCase):
    def test_epsilon(self):
        cmp = comparison.epsilon(1)

        assert cmp(1, 1)
        assert cmp(1, 2)
        assert not cmp(1, 3)
        assert cmp(2, 2)
        assert cmp(3, 2)

    def test_truthiness(self):
        cmp = comparison.truthiness

        assert cmp(True, True)
        assert cmp(False, False)
        assert not cmp(True, False)
        assert not cmp(False, True)
        assert cmp(1, [1])
        assert not cmp(1, [])
        
