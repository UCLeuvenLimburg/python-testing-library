from ucll_scripting.testing import *
import unittest


class ScoreTests(unittest.TestCase):

    def test_score_equality(self):
        assert Score(1, 1) == Score(1, 1)

    def test_score_inequality(self):
        assert Score(1, 1) != Score(1, 2)
        assert Score(3, 5) != Score(4, 5)

    def test_score_addition(self):
        assert Score(3, 5) + Score(2, 4) == Score(5, 9)
        assert Score(0, 0) + Score(2, 4) == Score(2, 4)

    def test_zero(self):
        assert Score(3, 5).zero == Score(0, 5)

    def test_rescale(self):
        assert Score(1, 2).rescale(4) == Score(2, 4)

    def test_perfect(self):
        assert Score(4, 4).is_perfect
        assert not Score(3, 4).is_perfect
