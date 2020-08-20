import os
import os.path
import sys


def remove_empty(directory):
    for path in os.listdir(directory):
        subdir = os.path.join(directory, path)
        if os.path.isdir(subdir):
            remove_empty(subdir)
    if not os.listdir(directory):
        print("Deleting directory {}".format(directory))
        os.rmdir(directory)


if __name__ == "__main__":
    remove_empty(sys.argv[1])
