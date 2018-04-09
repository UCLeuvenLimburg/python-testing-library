from ucll_scripting.dynload import load_code
from ucll_scripting.shell import test_directory
from ucll_scripting.dynvar import value
import os


def __load_module(filename, module_name, directory):
    # If no directory is specified, fetch the test file's directory
    if not directory:
        directory = value(test_directory)

    full_path = os.path.join(directory, filename)

    return load_code(full_path, module_name)
    

def load_student_module(filename='student.py', module_name='student', directory=None):
    return __load_module(filename, module_name, directory)

def load_reference_module(filename='solution.py', module_name='reference', directory=None):
    return __load_module(filename, module_name, directory)
