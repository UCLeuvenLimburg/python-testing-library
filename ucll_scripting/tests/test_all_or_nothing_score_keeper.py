from ucll_scripting.testing import *
import unittest


class AllOrNothingScoreKeeperTests(unittest.TestCase):
    def expect(self, expected, actual):
        assert expected == actual, f"Expected {expected}, got {actual}"
    
    def test_single_passing_test(self):
        def tested():
            with all_or_nothing():
                @test
                def _():
                    pass

        self.expect(Score(1, 1), score(tested))

    def test_single_failing_test(self):
        def tested():
            with all_or_nothing():
                @test
                def _():
                    fail()

        self.expect(Score(0, 1), score(tested))

    def test_single_skipping_test(self):
        def tested():
            with all_or_nothing(), when(never):
                @test
                def _():
                    pass

        self.expect(Score(0, 1), score(tested))
            
    def test_two_passing_tests(self):
        def tested():
            with all_or_nothing():
                @test
                def _():
                    pass

                @test
                def _():
                    pass
            
        self.expect(Score(2, 2), score(tested))

    def test_passing_and_failing_test(self):
        def tested():
            with all_or_nothing():
                @test
                def _():
                    pass

                @test
                def _():
                    fail()
            
        self.expect(Score(0, 2), score(tested))
            
    def test_failing_and_passing_test(self):
        def tested():
            with all_or_nothing():
                @test
                def _():
                    fail()

                @test
                def _():
                    pass
            
        self.expect(Score(0, 2), score(tested))
