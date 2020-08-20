"""
Copyright 2007 George Sakkis

The software is licensed according to the terms of the
PSF (Python Software Foundation) license found here:
http://www.python.org/psf/license/

https://code.activestate.com/recipes/499373/

"""
from __future__ import print_function
from builtins import str
from builtins import zip
from builtins import object
__all__ = ['fkdict']
__author__ = 'George Sakkis <george.sakkis AT gmail DOT com>'

from itertools import chain

class fkdict(object):
    '''A dict-like class for mappings with fixed keys.

    The main feature of this class is memory efficiency in the scenario of
    having many dicts with the same keys. Example use cases are rows read from a
    csv.DictReader or constructed out of rows fetched from a database. All such
    rows share the same keys() and therefore each row has to only hold the
    values().

    An additional feature is predictable ordering:
        fkdict.fromkeys('abcd').keys() == list('abcd')

    Currently fkdict does not support the dict operations that change the size
    of the container. Therefore, __delitem__(), pop(), popitem(), clear() and
    setdefault() are not provided. Also __setitem__() raises KeyError if the key
    does not already exist.
    '''

    __slots__ = ['_values']

    def __init__(self, seq=(), **kwds):
        # normalize arguments to a (key,value) iterable
        if hasattr(seq, 'keys'):
            get = seq.__getitem__
            seq = ((k,get(k)) for k in list(seq.keys()))
        if kwds:
            seq = chain(seq, iter(kwds.items()))
        # scan the items keeping track of the keys' order
        keys,values = [],[]
        keys_set = set()
        for k,v in seq:
            if k not in keys_set:
                keys_set.add(k)
                keys.append(k)
                values.append(v)
            else:
                values[keys.index(k)] = v
        # mutate self to the appropriate subclass
        self.__class__ = self._subcls_factory(*keys)
        self._values = values

    @classmethod
    def fromkeys(cls, keys, default=None):
        self = cls()
        self.__class__ = cls._subcls_factory(*keys)
        self._values = [default] * len(self)
        return self

    def __len__(self):
        return len(self._keys)

    def __contains__(self, key):
        return key in self._key2index

    def has_key(self, key):
        return key in self._key2index

    def __getitem__(self, key):
        return self._values[self._key2index[key]]

    def get(self, key, default=None):
        try: return self[key]
        except KeyError: return default

    def __setitem__(self, key, value):
        self._values[self._key2index[key]] = value

    def update(self, other=None, **kwargs):
        # copied from UserDict.DictMixin
        # Make progressively weaker assumptions about "other"
        if other is None:
            pass
        elif hasattr(other, 'iteritems'):
            for k, v in other.items():
                self[k] = v
        elif hasattr(other, 'keys'):
            for k in list(other.keys()):
                self[k] = other[k]
        else:
            for k, v in other:
                self[k] = v
        for k, v in kwargs.items():
            self[k] = v

    def __iter__(self):
        return iter(self._keys)

    def iterkeys(self):
        return iter(self._keys)

    def itervalues(self):
        return iter(self._values)

    def iteritems(self):
        return zip(self._keys, self._values)

    def keys(self):
        return list(self._keys)

    def values(self):
        return list(self._values)

    def items(self):
        return list(zip(self._keys, self._values))

    def copy(self):
        return self.__class__(iter(self.items()))

    def __eq__(self, other):
        return dict(iter(self.items())) == other

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        return '{%s}' % ', '.join('%r: %r' % item for item in iter(self.items()))

    @classmethod
    def _subcls_factory(cls, *keys):
        # if cls is hidden, find its first non hidden ancestor
        cls = next((c for c in cls.mro() if not issubclass(c,_Hidden)))
        # each (non hidden) class maintains its own registry
        try: registry = cls.__dict__['_Registry']
        except KeyError:
            registry = cls._Registry = {}
        try: return registry[keys]
        except KeyError:
            cls_name = '%s_%d' % (cls.__name__, abs(hash(keys)))
            cls_dict = {
                '__slots__' : (),
                '_keys' : keys,
                '_key2index' : dict((k,i) for i,k in enumerate(keys))
            }
            registry[keys] = sub = type(cls_name, (cls,_Hidden), cls_dict)
            return sub


class _Hidden(object):
    __slots__ = ()


dd = fkdict([('a', 4), ('b', 3)], c=8)
assert dd['a'] == 4
dd['b'] = 7
assert dd == {'a': 4, 'b': 7, 'c': 8}
assert not (dd != {'a': 4, 'b': 7, 'c': 8})
assert dd != {'a': 4, 'b': 7, 'c': 1}
assert not (dd == {'a': 4, 'b': 7, 'c': 1})
try:
    dd['d'] = 10
except KeyError:
    pass
assert dict(dd) == {'a': 4, 'c': 8, 'b': 7}
letters = fkdict.fromkeys('abc', 0)
assert letters == {'a': 0, 'b': 0, 'c': 0}
letters.update(b=4, c=5)
assert letters == {'a': 0, 'b': 4, 'c': 5}
letters.update({'b': 3})
assert letters == {'a': 0, 'b': 3, 'c': 5}
assert str(letters) == "{'a': 0, 'b': 3, 'c': 5}"
print("tests passed")
