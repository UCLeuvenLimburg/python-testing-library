from contextlib import contextmanager
from ucll_scripting.testing.core import *


def never():
    return False


def function_exists(function_name):
    '''
    Checks if a function with the given name exists in the given module.
    '''
    parts = function_name.split('.')
    current = globals()
    
    for part in parts[:-1]:
        if part in current:
            current = dir(current[part])
        else:
            return never
            
    return lambda: function_name in current



@contextmanager
def limit_failures(n = 1):
    '''
    Sets the condition to false once the given number of failed tests have been reached.
    '''
    failed_count = 0
    
    def failed():
        nonlocal failed_count
        failed_count += 1

    def condition():
        return failed_count < n

    with on_fail(failed), when(condition):
        yield
        
