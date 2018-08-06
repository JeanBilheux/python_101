# Full tutorial can be found here
# https://tutorialedge.net/python/concurrency/python-processpoolexecutor-tutorial/

from concurrent.futures import ProcessPoolExecutor
import os
from PIL import Image
import numpy as np
import glob
import time
import multiprocessing as mp


def read_file(file):
    print("Executing our task on process # {}".format(os.getpid()))
    data = np.array(Image.open(file))
    return data


def parallel(list_files):

    with ProcessPoolExecutor(max_workers=mp.cpu_count()) as executor:
        for _index, _data in zip(list_files, executor.map(read_file, list_files)):
            print("data[{}] = {}".format(_index, _data))



def normal(list_files):

    big_data_array = []
    for _index, _file in enumerate(list_files):
        data = read_file(_file)
        big_data_array.append(data)


if __name__ == "__main__":

    list_files = glob.glob('/Volumes/my_book_thunderbolt_duo/IPTS/IPTS-19921-Charles/114_without_registration/*.tif')
    list_files = list_files[:20]

    is_parallel = True

    start_time = time.time()

    if is_parallel:
        # parallel
        parallel(list_files)
    else:
        # method 1  - NO parallel
        normal(list_files)

    end_time = time.time()
    print("Loading using parallel={} mode took: {} s".format(is_parallel,
                                                             end_time- start_time))

# RESULT
    # no parallel took 14.24 s on MacPro
    # parallel took       on MacPro


