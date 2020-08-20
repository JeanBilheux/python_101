#!/usr/bin/env python
"""interleave.py <glob1> [, <glob1> ... ]

Accepts one of more files or globs interleaving lines and writing to stdout.

Copyright 2009 David Moss

Licensed under The MIT License:
https://opensource.org/licenses/MIT

https://code.activestate.com/recipes/576665/

"""
import os
import sys
import glob

def iter_interleave(*iterables):
    """
    A generator that interleaves the output from a one or more iterators
    until they are *all* exhausted.

    """
    iterables = list(map(iter, iterables))
    while iterables:
        result = []
        for it in iterables:
            try:
                result.append(next(it))
            except StopIteration:
                iterables.remove(it)
        for item in result:
            yield item

if __name__ == '__main__':
    files = []

    if len(sys.argv) < 2:
        print(__doc__.split("\n")[0])
        sys.exit(1)

    if sys.argv[1].lower() in ('-h', '--help'):
        print(__doc__, end='')
        sys.exit(0)

    for arg in sys.argv[1:]:
        for entry in glob.glob(arg):
            if os.path.isfile(entry):
                files.append(open(entry))

    for line in iter_interleave(*files):
        print(line, end='')
