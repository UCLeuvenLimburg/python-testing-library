class __Equality:
    def __init__(self, expected, actual):
        self.__expected = expected
        self.__actual = actual

    @property
    def success():
        return self.__expected == self.__actual

    @property
    def message():
        return f'Expected'

def equal(expected, actual):
    return expected == actual

def approximately_equal(epsilon=0.0001):
    return lambda expected, actual: abs(expected-actual) < epsilon

def truthy(actual):
    return True if actual else False

def falsey(actual):
    return False if actual else True

def same_truthiness(expected, actual):
    if is_truthy(expected):
        return truthy(actual)
    else:
        return falsey(actual)
