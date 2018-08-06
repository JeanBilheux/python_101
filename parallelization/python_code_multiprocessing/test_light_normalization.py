# hello.py

from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import glob
from PIL import Image
import numpy as np
import time

def my_func(list_files):

    array = []
    for _file in list_files:
        print("working with {}".format(_file))
        _image = Image.open(_file)
        _data = np.array(_image)
        array.append(_data)


def load_data(filename):
    print("working with {}".format(filename))
    _image = Image.open(filename)
    _data = np.array(_image)
    return _data

if __name__ == "__main__":
#    list_files = glob.glob('/Volumes/my_book_thunderbolt_duo/IPTS/IPTS-21115/Huggies_redo_subset/*.tiff')
    list_files = glob.glob('/Volumes/my_book_thunderbolt_duo/IPTS/IPTS-21115/Huggies_redo/*.tiff')
    print("Number of files to process: {}".format(len(list_files)))

    start_time = time.time()

    method = 3

    if method == 1:
        #    multi threading
        e = ProcessPoolExecutor()
        def load_data(filename):
            print("working with {}".format(filename))
            _image = Image.open(filename)
            _data = np.array(_image)
            return _data
        array = list(e.map(load_data, list_files))

    elif method == 2:
        # normal
        my_func(list_files)

    elif method == 3:

        pool = multiprocessing.Pool(processes=20)
        pool.map(load_data, list_files)

    end_time = time.time()
    print("It took {}".format(end_time - start_time))




