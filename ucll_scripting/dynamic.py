from contextlib import contextmanager


class __DynamicVariable:
    def __init__(self, initial_value):
        self.__value = initial_value

    @property
    def _value(self):
        return self.__value

    @_value.setter
    def _value(self, x):
        self.__value = x


def create_dynamic_variable(initial_value = None):
    return __DynamicVariable(initial_value)


@contextmanager
def let(dynamic_variable, value):
    old_value = dynamic_variable._value
    dynamic_variable._value = value

    try:
        yield
    finally:
        dynamic_variable._value = old_value


def value(dynamic_variable):
    return dynamic_variable._value
