from ucll_scripting.testing import *
import unittest


class CumulativeScoreKeeperTests(unittest.TestCase):
    def test_single_passing_test(self):
        def tested():
            @test
            def _():
                pass

        assert score(tested) == Score(1, 1)

    def test_single_failing_test(self):
        def tested():
            @test
            def _():
                fail()

        assert score(tested) == Score(0, 1)

    def test_single_skipping_test(self):
        def tested():
            with when(never):
                @test
                def _():
                    pass

        assert score(tested) == Score(0, 1)
            
    def test_two_passing_tests(self):
        def tested():
            @test
            def _():
                pass

            @test
            def _():
                pass
            
        assert score(tested) == Score(2, 2)

    def test_passing_and_failing_test(self):
        def tested():
            @test
            def _():
                pass

            @test
            def _():
                fail()
            
            assert score(tested) == Score(1, 2)

    pass
