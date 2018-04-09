from contextlib import contextmanager


class __DynamicVariable:
    def __init__(self, initial_value):
        self.__value = initial_value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, x):
        self.__value = x


def create_dynamic_variable(initial_value = None):
    return __DynamicVariable(initial_value)


@contextmanager
def let(dynamic_variable, value):
    old_value = dynamic_variable.value
    dynamic_variable.value = value

    try:
        yield
    finally:
        dynamic_variable.value = old_value

def value(dynamic_variable):
    return dynamic_variable.value
