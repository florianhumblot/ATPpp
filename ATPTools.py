from copy import deepcopy


def copyParameters(func):
    def passByValueFunction(*args):
        copied = [deepcopy(arg) for arg in args]
        return func(*copied)

    return passByValueFunction
