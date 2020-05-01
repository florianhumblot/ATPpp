from copy import deepcopy


# copyParameters :: Callable -> Callable
def copyParameters(func: callable) -> callable:
    """
    Decorator that copies the parameters of a function.
    """

    def passByValueFunction(*args):
        copied = [deepcopy(arg) for arg in args]
        return func(*copied)

    return passByValueFunction
