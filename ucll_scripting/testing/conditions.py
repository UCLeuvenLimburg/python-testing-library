import inspect
from contextlib import contextmanager
from ucll_scripting.testing.core import *


def never():
    return False


def always():
    return True


def function_exists(identifier, module = None):
    '''
    Checks if a variable with the given name exists.
    If no module is specified, the variable is looked for
    in the caller's environment (both locals and globals.)
    '''
    parts = identifier.split('.')

    if module:
        current = module.__dict__()
    else:
        caller_frame = inspect.currentframe().f_back
        locals = caller_frame.f_locals
        globals = caller_frame.f_globals
        current = { **locals, **globals }

    for part in parts[:-1]:
        if part in current:
            current = dir(current[part])
        else:
            return never

    if parts[-1] in current:
        return always
    else:
        return never



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
        
