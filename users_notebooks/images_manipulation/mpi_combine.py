# mpi_combine.py

import sys
from mpi4py import MPI
import glob
import numpy as np
import os
from pprint import pprint
import pyfits
import timeit

start_time = timeit.default_timer()

def get_list_files(folder):    
    '''
    returns the full list of fits files from the folder given
    '''
    list_files = glob.glob(folder + '/*.fits')
    return list_files
    
def digit_file_name(full_file_name):
    base_name = os.path.basename(full_file_name)
    [short_name, ext] = base_name.split('.')
    [image_name, image_sequence_number] = short_name.split('_')
    image_name_split = image_name.split('Image')
    image_number = image_name_split[1]
    return [image_name, image_number, image_sequence_number]

def get_list_files_to_add(index):
    final_list_files = []
    for data_list_files in full_list_images:
        _file = data_list_files[int(index)]
        final_list_files.append(_file)
    return final_list_files

def load_data(file):
    hdu_list = pyfits.open(file)
    hdu = hdu_list[0]
    return hdu.data

def write_data(file, data):
    hdu = pyfits.PrimaryHDU(data)
    hdu.writeto(file)

def add_images(start_index, end_index):
    '''
    Main Algorithm that add the files together
    '''
    for _index in np.arange(start_index, end_index):
        _add_data = []
        tmp_name = []
        image_sequnce_number = -1

        list_files_to_add = get_list_files_to_add(_index)
        for _index2, _file in enumerate(list_files_to_add):
#            [image_name, image_number, image_sequence_number] = digit_file_name(_file)
#            image_name = 'all_images'
#            image_number = _index
            _data = load_data(_file)
            if _index2  == 0:
                _add_data = _data
#                _tmp_name = "%.2d" %int(image_number)
#            else:
                _add_data += _data
#                _tmp_name += '_%.2d' %int(image_number)
    
#        full_name = os.path.join(output_folder, _tmp_name + '_' + image_sequence_number + '.fits')
        full_name = os.path.join(output_folder, "all_data_{:04d}".format(int(_index)) + '.fits')
        write_data(full_name, _add_data)

def mean_images(start_index, end_index):
    '''
    Main Algorithm that get the mean 
    '''
    for _index in np.arange(start_index, end_index):
        _add_data = []
        tmp_name = []
        image_sequnce_number = -1

        list_files_to_add = get_list_files_to_add(_index)
        nbr_files_to_add = len(list_files_to_add)
        for _index, _file in enumerate(list_files_to_add):
            [image_name, image_number, image_sequence_number] = digit_file_name(_file)
            _data = load_data(_file)
            if _index  == 0:
                _add_data = _data
                _tmp_name = "%.2d" %int(image_number)
            else:
                _add_data += _data
                _tmp_name += '_%.2d' %int(image_number)
    
        _add_data = _add_data / float(nbr_files_to_add)
        full_name = os.path.join(output_folder, _tmp_name + '_' + image_sequence_number + '.fits')
        write_data(full_name, _add_data)

def median_images(start_index, end_index):
    '''
    Main Algorithm that get the median of several arrays
    '''
    for _index in np.arange(start_index, end_index):
        _add_data = []
        tmp_name = []
        image_sequnce_number = -1

        list_files_to_add = get_list_files_to_add(_index)
        nbr_files_to_add = len(list_files_to_add)
        _median_data = []
        for _index, _file in enumerate(list_files_to_add):
            [image_name, image_number, image_sequence_number] = digit_file_name(_file)
            _data = load_data(_file)
            _median_data.append(_data)
            if _index == 0:
                _tmp_name = '%.2d' %int(image_number)
            else:
                _tmp_name += '_%.2d' %int(image_number)
    
        median_data = np.median(_median_data, axis=0)
        full_name = os.path.join(output_folder, _tmp_name + '_' + image_sequence_number + '.fits')
        write_data(full_name, median_data)

           
if len(sys.argv) < 4:
    raise ValueError("At least 4 arguments required! 1 algorithm ('add', 'mean' or 'median') \
                     2 input folders and 1 output folder.")

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
nbr_cpu = comm.Get_size()

algorithm = sys.argv[1]
input_folders = sys.argv[2:-1]
output_folder = sys.argv[-1]

print("=>>>> Process #{}".format(rank))
#print("algorithm: %s" %algorithm)
#print("input_folders %s" %input_folders)

# collect list of images
full_list_images = []
for _folder in input_folders:
    _list_files = get_list_files(_folder)
    full_list_images.append(_list_files)

print("full_list_images:")
print(full_list_images)
    
# Calculate all the bins size
nbr_files_per_folder = len(full_list_images[0])
bin_sized = np.ceil(nbr_files_per_folder / nbr_cpu)

bins = np.ones((nbr_cpu))*bin_sized
bins[-1] = nbr_files_per_folder - np.sum(bins[0:-1])

# list of indexes for this rank
if rank == 0:
    start_index = 0
    end_index = bins[1]
else:
    start_index = np.sum(bins[0:rank])
    end_index = start_index + bins[rank]
#print("rank:%d  start_index:%d  end_index:%d"%(rank, start_index, end_index))

if algorithm == 'add':
    add_images(start_index, end_index)
elif algorithm == 'mean':
    mean_images(start_index, end_index)
elif algorithm == 'median':
    median_images(start_index, end_index)
else:
    raise("Algorithm Key Error")

end_time = timeit.default_timer()
if rank == 0:
    print("Process time: %ds" % (end_time - start_time))

#Code to test
#mpiexec -n 4 python mpi_combine.py add /Volumes/my_book_thunderbolt_duo/IPTS/BraggEdge/SNAP/April9_2015/Overnight_Scan_DOE_Si_powder/Corrected_Images015 /Volumes/my_book_thunderbolt_duo/IPTS/BraggEdge/SNAP/April9_2015/Overnight_Scan_DOE_Si_powder/Corrected_Images016 /Volumes/my_book_thunderbolt_duo/IPTS/BraggEdge/SNAP/April9_2015/Overnight_Scan_DOE_Si_powder/Corrected_Images017 /Users/j35/Desktop/remove_me
