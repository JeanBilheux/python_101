import os.path


def parents(filename):
    path = os.path.abspath(filename)
    while os.path.dirname(path) != path:
        path = os.path.dirname(path)
        yield path


def find_configs(filename):
    config_files = [
        os.path.join(path, '.editorconfig')
        for path in parents(filename)
    ]
    return [
        (path, open(path).read())
        for path in config_files
        if os.path.isfile(path)
    ]

