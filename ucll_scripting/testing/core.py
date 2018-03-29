from contextlib import contextmanager
from ucll_scripting.dynamic import create_dynamic_variable, let, value


def do_nothing():
    pass

__condition = create_dynamic_variable( lambda: True )
__passed = create_dynamic_variable( do_nothing )
__failed = create_dynamic_variable( do_nothing )
__skipped = create_dynamic_variable( do_nothing )


class __TestFailure(Exception):
    pass

class __InvalidCallError(Exception):
    pass


def fail():
    raise __TestFailure()


def __should_test_run():
    return value(__condition)()

def __chain(f, g):
    def chain():
        f()
        g()

    return chain


@contextmanager
def __add_callback(event, callback):
    '''
    Helper function. Adds a callback to and event,
    the event being __passed, __failed or __skipped.
    '''
    old_callback = value(event)
    chained = __chain(old_callback, callback)

    with let(event, chained):
        yield

@contextmanager
def on_pass(callback):
    '''
    Adds a callback to the on-pass chain.
    '''
    with __add_callback(__passed, callback):
        yield

@contextmanager
def on_fail(callback):
    '''
    Adds a callback to the on-fail chain.
    '''
    with __add_callback(__failed, callback):
        yield

@contextmanager
def on_skip(callback):
    '''
    Adds a callback to the on-skip chain.
    '''
    with __add_callback(__skipped, callback):
        yield

@contextmanager
def when(condition):
    '''
    Adds an extra condition'
    '''
    old_condition = value(__condition)
    
    with let(__condition, lambda: old_condition() and condition()):
        yield
   
def __run_test(test_function):
    def signal_passed():
        value(__passed)()

    def signal_failed():
        value(__failed)()

    def signal_skipped():
        value(__skipped)()
        
    if __should_test_run():
        try:
            test_function()
            signal_passed()
        except __TestFailure:
            signal_failed()
    else:
        signal_skipped()

def test(test_function):
    '''
    Decorator for test functions.
    '''
    def dummy():
        raise __InvalidCallError('Functions decorated with @test should never be called')
    
    __run_test(test_function)

    return dummy
