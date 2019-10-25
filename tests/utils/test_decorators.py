"""
Simple decorator to print a function doc string.
"""
import functools


def it(func):
    """
    Prints the doc string for you
    """
    @functools.wraps(func)
    def wrapper_print_doc_str(*args, **kwargs):
        print(func.__doc__)
        return func(*args, **kwargs)
    return wrapper_print_doc_str


def describe(cls):
    """
    Prints the class doc string
    """
    print(cls.__doc__)
    return cls
