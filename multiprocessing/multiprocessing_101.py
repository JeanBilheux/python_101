# https://www.datacamp.com/tutorial/python-multiprocessing-tutorial

import numpy as np
from skimage.io import imread
from tqdm import tqdm
import glob, os
import multiprocessing as mp

def worker(fl):
    return (imread(fl).astype(np.float32)).swapaxes(0,1)

def hype_loader_sum(fls_lst):
    with mp.Pool(processes=10) as pool:
        data = pool.map(worker, fls_lst)

    return np.array(data).sum(axis=0)[10:-10, 10:-10]


# load a data
fld_path = ('/Volumes/JeanHardDrive/SNS/SNAP/IPTS-27829-Adrian')
fld_lst = glob.glob(os.path.join(fld_path, 'run*')) # find all projections
fld_lst.sort()

print(fld_lst)

projs = []
for fld in tqdm(fld_lst):
    fls_lst = glob.glob(os.path.join(fld, '*.tif*'))
    fls_lst.sort()
    projs.append(hype_loader_sum(fls_lst))