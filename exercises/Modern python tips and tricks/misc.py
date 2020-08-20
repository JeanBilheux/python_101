"""Miscellaneous exercises"""
from functools import wraps
from itertools import cycle



def count_calls(func):
    """Pass call counts into first argument to the function."""
    @wraps(func)
    def new_func(*args):
        new_func.call_count += 1
        return func(new_func.call_count, *args)
    new_func.call_count = 0
    return new_func


def deep_flatten(thing):
    try:
        for item in thing:
            if isinstance(item, (str, bytes)):
                yield item
            else:
                for x in deep_flatten(item):
                    yield x
    except TypeError:
        yield thing


class PermaDict(dict):

    """Mapping that doesn't allow updating keys once set."""

    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"{key} already in dictionary.")
        super().__setitem__(key, value)

    def update(self, obj=(), **kwargs):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in self:
                    raise KeyError(f"{key} already in dictionary.")
                super().__setitem__(key, value)
        else:
            for key, value in obj:
                if key in self:
                    raise KeyError(f"{key} already in dictionary.")
                super().__setitem__(key, value)
        for key, value in kwargs.items():
            if key in self:
                raise KeyError(f"{key} already in dictionary.")
            super().__setitem__(key, value)


class OrderedSet:

    """Set-like object that maintains insertion order of items."""

    def __init__(self, iterables):
        self.items = dict.fromkeys(iterables, None)

    def __contains__(self, item):
        return item in self.items

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items.keys())

    def add(self, item):
        self.items[item] = None

    def discard(self, item):
        self.items.pop(item, None)

    def remove(self, item):
        del self.items[item]

    def clear(self):
        self.items.clear()


class CyclicList:

    """List-like data structure that loops in a cyclic manner."""

    def __init__(self, iterable=()):
        self.data = list(iterable)

    def __iter__(self):
        return cycle(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index % len(self)]

    def __setitem__(self, i, v):
        self.data[i % len(self)] = v

    def append(self, item):
        self.data.append(item)

    def pop(self, index=-1):
        return self.data.pop(index)
