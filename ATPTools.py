from copy import deepcopy


# copyParameters :: Callable -> Callable
def copyParameters(func: callable) -> callable:
    """
    Decorator that makes a deepcopy the parameters of a function before passing them to prevent pass-by-reference calls.
    """
    # passByValueFunction :: Any -> Callable[[_], Any] -> Any?
    def passByValueFunction(*args):
        copied = [deepcopy(arg) for arg in args]
        return func(*copied)

    return passByValueFunction
