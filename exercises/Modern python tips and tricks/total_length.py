from operator import length_hint


def total_length(*iterables, use_hints=False):
    length = 0
    for iterable in iterables:
        try:
            length += len(iterable)
        except TypeError:
            hint = length_hint(iterable)
            if use_hints and hint:
                length += hint
            else:
                length += sum(1 for _ in iterable)
    return length
