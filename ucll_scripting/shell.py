from contextlib import contextmanager
from ucll_scripting.testing import *
from ucll_scripting.dynvar import *
import ucll_scripting.testing.reporting as reporting
from ucll_scripting.testing.counting import *
import argparse
import sys
import os


test_filename = create_dynamic_variable()
test_directory = create_dynamic_variable()

@contextmanager
def __extended_python_path(path):
    old = sys.path

    try:
        sys.path.append(path)
        yield
    finally:
        sys.path = old



def __parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--limit", help="stop after N failures", type=int, default=0, dest='max_failure_count', metavar='N')
    parser.add_argument("--tests", help="name of file containing tests", default='tests.py', dest='tests_filename', metavar='FILE')

    return parser.parse_args()


def __subdirectories(root = '.'):
    yield root

    for entry in os.listdir(root):
        path = os.path.join(root, entry)

        if os.path.isdir(path):
            yield from __subdirectories(path)


def __contains_tests(subdirectory, filename):
    path = os.path.join(subdirectory, filename)
    return os.path.isfile(path)

def __find_tests_in_subdirectories(filename, root='.'):
    return ( os.path.join(subdirectory, filename) for subdirectory in __subdirectories(root) if __contains_tests(subdirectory, filename) )

def __create_test_runner(paths):
    def run_single(test_file_path):
        with open(test_file_path, 'r') as file:
            source = file.read()
            
        absolute_test_file_path = os.path.abspath(test_file_path)
        absolute_test_directory_path = os.path.dirname(absolute_test_file_path)

        with __extended_python_path(absolute_test_directory_path), \
             let (test_filename, absolute_test_file_path),         \
             let (test_directory, absolute_test_directory_path):
            global_bindings = {}
            exec(source, global_bindings)

    def run_all():
        for path in paths:
            run_single(path)

    return run_all

def run_tests():
    arguments = __parse_command_line_arguments()
    paths = __find_tests_in_subdirectories(arguments.tests_filename)
    test_runner = __create_test_runner(paths)

    if arguments.max_failure_count:
        def add_limit(cont):
            def go():
                with limit_failures(arguments.max_failure_count):
                    cont()

            return go

        test_runner = add_limit(test_runner)

    print(reporting)
    with reporting.setup(), count_passes() as passes, count_fails() as fails, count_skips() as skips:
        end_score = score(test_runner)
        print('=' * 40)
        print(f'{passes.count} pass(es), {fails.count} failure(s), {skips.count} skip(s)')
        print(f'Total score: {end_score}')
