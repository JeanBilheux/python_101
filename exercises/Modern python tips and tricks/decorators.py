"""Decorator exercises"""
from functools import wraps


def catch_all(func):
    """Trap non-exiting errors and ask user if we should ignore."""
    @wraps(func)
    def new_func(*args):
        try:
            return func(*args)
        except Exception as error:
            print("Exception occurred: {}".format(error))
            answer = input("Should we ignore this exception (Y/n)? ")
            if answer.lower() == "n":
                raise
    return new_func
