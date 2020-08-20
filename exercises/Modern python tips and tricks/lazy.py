"""Laziness exercises"""


def reverse_difference(numbers):
    """Return list of reversed numbers subtracted from itself."""
    differences = []
    for i in range(len(numbers)):
        differences.append(numbers[i] - numbers[-(i+1)])
    return differences


def get_shared_keys(dict1, dict2):
    """Return the keys that are shared by both dictionaries."""
    shared = set()
    for key in dict1:
        if key in dict2:
            shared.add(key)
    return shared
