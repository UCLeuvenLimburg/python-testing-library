from contextlib import contextmanager
from ucll_scripting.testing import *
import argparse
import sys
import os


@contextmanager
def extended_python_path(path):
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
    def run_single(path):
        with open(path, 'r') as file:
            source = file.read()
            full_path = os.path.abspath(path)

            with extended_python_path(os.path.dirname(full_path)):
                exec(source, {})

    def run_all():
        for path in paths:
            run_single(path)

    return run_all

def run_tests():
    def printer(message):
        return lambda: print(message)

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

    with on_pass(printer('pass')), on_fail(printer('fail')), on_skip(printer('skip')):
        print(score(test_runner))
