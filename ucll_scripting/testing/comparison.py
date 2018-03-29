def equality(x, y):
    return x == y


def epsilon(e):
    def compare(x, y):
        return abs(x-y) <= e

    return compare


def truthiness(x, y):
    if x and y:
        return True

    if (not x) and (not y):
        return True

    return False
