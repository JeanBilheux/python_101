import os
import sys


def list_files(directory):
    for path in sorted(os.listdir(directory)):
        print(path)


if __name__ == "__main__":
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    list_files(directory)
