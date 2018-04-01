import types


def create_empty_module(name):
    return types.ModuleType(name)

def execute_into_module(source, module):
    exec(source, module.__dict__)
    return module

def load_code(filename, module_name):
    m = create_empty_module(module_name)

    with open(filename, 'r') as file:
        code = file.read()
        execute_into_module(code, m)

    return m
