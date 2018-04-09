from contextlib import contextmanager
from ucll_scripting.testing import *


class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


def __incrementer(counter):
    return lambda *args, **kwargs: counter.increment()
        

@contextmanager
def count_passes():
    counter = Counter()
    
    with on_pass(__incrementer(counter)):
        yield counter


@contextmanager
def count_fails():
    counter = Counter()
    
    with on_fail(__incrementer(counter)):
        yield counter


@contextmanager
def count_skips():
    counter = Counter()
    
    with on_skip(__incrementer(counter)):
        yield counter
