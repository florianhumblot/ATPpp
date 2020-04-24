from copy import deepcopy


def copyParameters(func):
    """
    Decorator that copies the parameters of a function.
    """
    def passByValueFunction(*args):
        copied = [deepcopy(arg) for arg in args]
        return func(*copied)

    return passByValueFunction
