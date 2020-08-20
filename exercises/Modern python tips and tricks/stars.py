"""Star exercises"""
import sys


def dict_from_tuple(tuples):
    """Turn three-item tuples into a dictionary of two-valued tuples."""
    truple_dict = {}
    for items in tuples:
        key, values = items[0], items[1:]
        truple_dict[key] = tuple(values)
    return truple_dict


def print(*values, **kwargs):
    unknown = set(kwargs.keys()) - {'sep', 'end', 'file', 'flush'}
    out = kwargs.get('file', sys.stdout)
    if unknown:
        print("Unknown keyword arguments given: ", ', '.join(unknown))
    out.write(kwargs.get('sep', ' ').join(str(v) for v in values))
    out.write(kwargs.get('end', '\n'))
    if kwargs.get('flush', False):
        out.flush()
