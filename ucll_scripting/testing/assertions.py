class Result:
    pass

class Success(Result):
    def __bool__(self):
        return True

    def __and__(self, other):
        return other

    def __or__(self, other):
        return self


class Failure(Result):
    def __init__(self, reason):
        self.__reason = reason
    
    def __bool__(self):
        return False

    @property
    def reason(self):
        return self.__reason

    def __and__(self, other):
        return self

    def __or__(self, other):
        return other


def equal(*, expected, actual):
    if expected == actual:
        return Success()
    else:
        return Failure(f'Expected value: {expected}, actual value: {actual}')


def equal_with_absolute_error(*, expected, actual, epsilon=0.0001):
    if abs(expected-actual) < epsilon:
        return Success()
    else:
        return Failure(f'Expected value: {expected} +- {epsilon}, actual value: {actual}')


def equal_with_relative_error(*, expected, actual, percentage=0.01):
    if (1 - percentage) * expected < actual < (1 + percentage) * expected:
        return Success()
    else:
        return Failure(f'Expected value: {expected} +- {percentage}%, actual value: {actual}')


def truthy(*, actual):
    if actual:
        return Success
    else:
        return Failure(f'Value {actual} is expected to be truthy')


def falsey(*, actual):
    if not actual:
        return Success
    else:
        return Failure(f'Value {actual} is expected to be falsye')

    
def same_truthiness(*, expected, actual):
    if expected:
        return truthy(actual=actual)
    else:
        return falsey(actual=actual)



