from collections.abc import Mapping


def flatten_dict(dictionary, sep="_"):
    flattened = {}
    for key, value in dictionary.items():
        if isinstance(value, Mapping):
            inner_dict = flatten_dict(value, sep=sep)
            for inner_key, inner_value in inner_dict.items():
                flattened[f"{key}{sep}{inner_key}"] = inner_value
        else:
            flattened[key] = value
    return flattened


def pluck(dictionary, *key_paths, **kwargs):
    """Deep-query a dictionary"""
    values = []
    for path in key_paths:
        obj = dictionary
        for key in path.split(kwargs.get('sep', '.')):
            try:
                obj = obj[key]
            except KeyError:
                if 'default' in kwargs:
                    obj = kwargs['default']
                    break
                else:
                    raise
        values.append(obj)
    if len(key_paths) == 1:
        return values[0]
    else:
        return tuple(values)
