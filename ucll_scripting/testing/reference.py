from contextlib import contextmanager
from ucll_scripting.dynamic import create_dynamic_variable, let, value
from ucll_scripting.testing import *


@contextmanager
def check_function_against_reference_implementation(*, tested, reference):
    def testcase(*args, **kwargs):
        @test
        def _():
            actual = tested(*args, **kwargs)
            expected = reference(*args, **kwargs)

            if actual != expected:
                fail()

    yield testcase
