from ucll_scripting.testing import *
import unittest


class AllOrNothingiScoreKeeperTests(unittest.TestCase):
    def expect(self, expected, actual):
        assert expected == actual, f"Expected {expected}, got {actual}"
    
    def test_single_passing_test(self):
        def tested():
            with weight(5):
                @test
                def _():
                    pass

        self.expect(Score(5, 5), score(tested))

    def test_single_failing_test(self):
        def tested():
            with weight(3):
                @test
                def _():
                    fail()

        self.expect(Score(0, 3), score(tested))

    def test_single_skipping_test(self):
        def tested():
            with weight(10), when(never):
                @test
                def _():
                    pass

        self.expect(Score(0, 10), score(tested))
            
    def test_two_passing_tests(self):
        def tested():
            with weight(7):
                @test
                def _():
                    pass

                @test
                def _():
                    pass
            
        self.expect(Score(7, 7), score(tested))

    def test_passing_and_failing_test(self):
        def tested():
            with weight(8):
                @test
                def _():
                    pass

                @test
                def _():
                    fail()
            
        self.expect(Score(4, 8), score(tested))
            
    def test_failing_and_passing_test(self):
        def tested():
            with weight(20):
                @test
                def _():
                    fail()

                @test
                def _():
                    pass
            
        self.expect(Score(10, 20), score(tested))
