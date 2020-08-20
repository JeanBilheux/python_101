import gzip
try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen
from io import BytesIO
import sys


def save_gzipped_data(url, filename):
    response = BytesIO(urlopen(url).read())
    with gzip.GzipFile(fileobj=response) as extracted:
        with open(filename, mode='wb') as data_file:
            data_file.write(extracted.read())


if __name__ == "__main__":
    url, filename = sys.argv[1:]
    save_gzipped_data(url, filename)
