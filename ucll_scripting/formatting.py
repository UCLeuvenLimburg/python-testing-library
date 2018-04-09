class __String:
    def __init__(self, string):
        self.__string = string

    def format(self):
        return [ self.__string ]


class __HorizontalBox:
    def __init__(self, children, aligner):
        self.__children = children
        self.__aligner = aligner

    def format(self):
        columns = [ child.format() for child in self.__children ]
        height = max([0] + [len(column) for column in columns])

        for column in columns:
            width = max(len(line) for line in column)

            for i in range(len(column)):
                column[i] = self.__aligner(column[i], width)

            column += [ " " * width ] * (height - len(column))

        return [ "".join(columns[i][j] for i in range(len(columns))) for j in range(height) ]
                


class __VerticalBox:
    def __init__(self, children):
        self.__children = children

    def format(self):
        return [ line for child in self.__children for line in child.format() ]


def __wrap_string(x):
    if type(x) is str:
        return __String(x)
    else:
        return x


def __wrap_strings(xs):
    return [ __wrap_string(x) for x in xs ]


class HorizontalAlignment:
    @staticmethod
    def left(string, width):
        return string.ljust(width)

    @staticmethod
    def right(string, width):
        return string.rjust(width)

    @staticmethod
    def center(string, width):
        total_margin = width - len(string)
        right_margin = total_margin // 2
        left_margin = total_margin - right_margin

        return ' ' * left_margin + string + ' ' * right_margin


def hbox(*children, halign=HorizontalAlignment.left):
    return __HorizontalBox(__wrap_strings(children), halign)


def vbox(*children):
    return __VerticalBox(__wrap_strings(children))


def indent(n, child):
    indentation = " " * n
    return hbox(indentation, __wrap_string(child))
