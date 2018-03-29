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


def run_tests():
    def run(filename):
        with open(filename, 'r') as file:
            source = file.read()
            full_path = os.path.abspath(filename)

            with extended_python_path(os.path.dirname(full_path)):
                exec(source, {})


    parser = argparse.ArgumentParser()

    parser.add_argument("--limit", help="stop after N failures", type=int, default=0, dest='max_failure_count', metavar='N')
    parser.add_argument("--tests", help="name of file containing tests", default='tests.py', dest='tests_file', metavar='FILE')
    arguments = parser.parse_args()

    test_runner = lambda: run(arguments.tests_file)

    if arguments.max_failure_count:
        def add_limit(cont):
            def go():
                with limit_failures(arguments.max_failure_count):
                    cont()

            return go

        test_runner = add_limit(test_runner)

    print(score(test_runner))
