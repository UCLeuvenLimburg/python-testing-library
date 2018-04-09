from contextlib import contextmanager
from ucll_scripting.dynvar import create_dynamic_variable, let, value
from ucll_scripting.testing.core import *
import ucll_scripting.formatting as format


__failure_message_generator = create_dynamic_variable()


def __dummy_failure_message_generator(**kwargs):
    raise Exception("Bug in tests: no failure message generator defined")


@contextmanager
def failure_message_generator(message_generator):
    with let(__failure_message_generator, message_generator):
        yield


@contextmanager
def default_failure_message_generator(message_generator):
    if value(__failure_message_generator) != __dummy_failure_message_generator:
        yield
    else:
        with failure_message_generator(message_generator):
            yield


@contextmanager
def failure_message(message):
    def generator(**kwargs):
        return message.format(**kwargs)

    with failure_message_generator(generator):
        yield


@contextmanager
def default_failure_message(message):
    def generator(**kwargs):
        return message.format(**kwargs)

    with default_failure_message_generator(generator):
        yield


@contextmanager
def setup():
    failure_index = 1
    
    def failure_callback(*, failure):
        nonlocal failure_index
        
        if failure_index != 1:
            print('-' * 40)

        generator = value(__failure_message_generator)
        message = generator(failure=failure)
        message_lines = format.hbox(f'[{failure_index}] ', message).format()
        print("\n".join(message_lines))

        failure_index += 1
            
    with let(__failure_message_generator, __dummy_failure_message_generator), on_fail(failure_callback):
        yield
