from contextlib import contextmanager
from ucll_scripting.dynvar import create_dynamic_variable, let, value
from ucll_scripting.testing import *
import ucll_scripting.formatting as format
import ucll_scripting.testing.reporting as reporting
from ucll_scripting.testing.assertions import *
from copy import deepcopy
import inspect

tested_function_name = create_dynamic_variable()
__failure_message = create_dynamic_variable()


def __get_positional_parameter_names(function):
    return inspect.getargspec(function)[0]


@contextmanager
def check_function_against_reference_implementation(*, tested, reference, comparison=None):
    def check(*args, **kwargs):
        positional_parameter_names = __get_positional_parameter_names(reference)
        function_name = value(tested_function_name)
        positional_argument_strings = [ str(arg) for arg in args ]
        keyword_argument_strings = [ f'{k}={v}' for k, vi in kwargs.items() ]
        arguments_string = ', '.join(positional_argument_strings + keyword_argument_strings)
        call_string = f'{function_name}({arguments_string})'

        def failure_message_generator(*, failure, **kwargs):
            failure_message = value(__failure_message)
            
            if failure_message:
                return format.vbox(f'Verifying {call_string}', \
                                   format.indent(2, failure_message), \
                                   format.indent(2, str(failure)))
            else:
                raise Exception('Bug in reference tests: no failure message set')
        
        def test_function():
            tested_args = deepcopy(args)
            tested_kwargs = deepcopy(kwargs)
            reference_args = deepcopy(args)
            reference_kwargs = deepcopy(kwargs)

            __failure_message.value = f'Exception occurred during function call'
            
            actual_result = tested(*tested_args, **tested_kwargs)
            expected_result = reference(*tested_args, **tested_kwargs)

            __failure_message.value = f'Comparing return values'
            assert expected_result == actual_result, f'Expected {expected_result}, got {actual_result}'

            for i in range(len(args)):
                parameter_name = positional_parameter_names[i]
                __failure_message.value = f'Comparing {parameter_name} (positional argument #{i+1})'

                expected = reference_args[i]
                actual = tested_args[i]
                assert expected == actual, f'Expected {expected}, got {actual}'
                

        with reporting.default_failure_message_generator(failure_message_generator), \
             let(__failure_message, None):
            test(test_function)

    yield check


reference_module = create_dynamic_variable()
tested_module = create_dynamic_variable()

@contextmanager
def function_reftest(identifier):
    if not identifier in dir(value(reference_module)):
        raise Exception(f'Bug in tests: reference module does not contain member called "{identifier}"')
    
    with when(defined(identifier, value(tested_module))), let(tested_function_name, identifier):
        reference_function = getattr(value(reference_module), identifier)
        tested_function = getattr(value(tested_module), identifier)

        with check_function_against_reference_implementation(tested=tested_function, reference=reference_function) as check:
            yield check
