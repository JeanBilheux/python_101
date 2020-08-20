import os
import re
import sys


def print_tree(top, prefix=""):
    """Print paths for file tree recursively."""
    print(prefix + os.path.basename(top))
    prefix = re.sub(r"[-`]", " ", prefix)
    try:
        children = os.listdir(top)
    except OSError:
        return  # This is a file, not a directory
    if not children:
        return  # Empty directory
    children = sorted(os.path.join(top, name) for name in children)
    for name in children[:-1]:
        print_tree(name, (prefix + "|-- "))
    print_tree(children[-1], (prefix + "`-- "))


if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    print_tree(directory)
