from collections.abc import Iterable


def deep_add(numbers, start=0):
    """Return sum of values in given iterable, iterating deeply."""
    total = start
    for value in numbers:
        if isinstance(value, Iterable):
            total = deep_add(value, start=total)
        else:
            total += value
    return total
