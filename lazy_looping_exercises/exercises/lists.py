"""List comprehension exercises"""


def get_vowel_names(names):
    """Return a list containing all names given that start with a vowel."""
#    return [_string for _string in names if _string[0].lower() in ['a', 'e', 'i', 'o', 'u']]
    return [_string
            for _string in names
            if _string.lower().startswith(tuple('aeiou'))]


def flatten():
    """Return a flattened version of the given 2-D matrix (list-of-lists)."""


def matrix_from_string():
    """Convert rows of numbers to list of lists."""


def power_list():
    """Return a list that contains each number raised to the i-th power."""


def matrix_add():
    """Add corresponding numbers in given 2-D matrices."""


def identity():
    """Return an identity matrix of size x size."""


def triples():
    """Return list of Pythagorean triples less than input num."""
