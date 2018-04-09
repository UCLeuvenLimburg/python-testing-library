from contextlib import contextmanager
from ucll_scripting.dynvar import create_dynamic_variable, let, value


def do_nothing(*args, **kwargs):
    pass

__condition = create_dynamic_variable(lambda: True)
__passed = create_dynamic_variable(do_nothing)
__failed = create_dynamic_variable(do_nothing)
__skipped = create_dynamic_variable(do_nothing)
__test_function = create_dynamic_variable()


class __InvalidCallError(Exception):
    pass


def __should_test_run():
    return value(__condition)()


def __chain(f, g):
    def chain(*args, **kwargs):
        f(*args, **kwargs)
        g(*args, **kwargs)

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
    Adds an extra condition
    '''
    old_condition = value(__condition)
    
    with let(__condition, lambda: old_condition() and condition()):
        yield
   
def __run_test(test_function):
    def signal_passed():
        value(__passed)()

    def signal_failed(exception):
        value(__failed)(failure=exception)

    def signal_skipped():
        value(__skipped)()

    if __should_test_run():
        with let(__test_function, test_function):
            try:
                test_function()
                signal_passed()
            except NotImplementedError:
                signal_skipped()
            except BaseException as e:
                signal_failed(e)
    else:
        signal_skipped()

def current_test_function():
    # Inside a @test annotated function, returns the function
    return value(__test_function)
        
def test(test_function):
    '''
    Decorator for test functions.
    '''
    def dummy():
        raise __InvalidCallError('Functions decorated with @test should never be called')
    
    __run_test(test_function)

    return dummy


class TestData:
    def __init__(self, dictionary = None):
        object.__setattr__(self, '__dictionary', dictionary if dictionary else {})
    
    def __getattr__(self, name):
        return object.__getattribute__(self, '__dictionary')[name]

    def __setattr__(self, name, value):
        dic = object.__getattribute__(self, '__dictionary')
        
        if name in dic.keys():
            raise Exception("Cannot set same test data variable twice within same test")
        else:
            dic[name] = value

    def __str__(self):
        return str(object.__getattribute__(self, '__dictionary'))
