# import glob
# import os
# from PIL import Image
# import time
# import numpy as np
#
# import concurrent.futures
#
#
# list_files = glob.glob("/Users/j35/HFIR/CG1D/IPTS-30750/23_06_09_left/*.tiff")    # 529 images
# assert len(list_files) > 0
#
# # def loading_indexes(from_index=0, to_index=1):
# #     time.sleep(1)
#     # local_array = []
#     # for _file in list_files[from_index: to_index]:
#     #     local_array.append(np.array(Image.open(_file)))
#     # return f"{from_index} - {to_index} : Done!"
#
# def useless_function(sec):
#     time.sleep(sec)
#     return sec
#
#
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     process1 = executor.submit(useless_function, 1)
#     process2 = executor.submit(useless_function, 1)
#
#     # process1 = executor.submit(loading_indexes, 0, 100)
#     # process2 = executor.submit(loading_indexes, 100, 200)
#     # process3 = executor.submit(loading_indexes, 200, 300)
#     # process4 = executor.submit(loading_indexes, 300, 400)
#     # process5 = executor.submit(loading_indexes, 400, 529)
#

import concurrent.futures
import glob
import numpy as np
from PIL import Image
import time

list_files = glob.glob("/Users/j35/HFIR/CG1D/IPTS-30750/23_06_09_left/*.tiff")    # 529 images
assert len(list_files) > 0


# Retrieve a single page and report the URL and contents
def loading_indexes(file_index):
    print(f"{file_index = }")
    time.sleep(1)
    return 1

nbr_files_per_thread = 50
def loading_images(from_index, output_folder):
    _list_files = list_files[from_index * nbr_files_per_thread: (from_index + 1) * nbr_files_per_thread]
    print(f"{from_index =}: loading {len(_list_files)} files to export in {output_folder}")
    local_list_images = []
    for _file in _list_files:
        local_list_images.append(np.array(Image.open(_file)))

    time.sleep(5)

    return {'array': local_list_images,
            'index': from_index}


# start_time = time.perf_counter()
# for _file in list_files[0: 500]:
#     _array = np.array(Image.open(_file))
# end_time = time.perf_counter()
# print(f"It took {end_time - start_time}s in serial")


start_time = time.perf_counter()
# We can use a with statement to ensure threads are cleaned up promptly
global_data = {}

output_folder = "this is the output folder"
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    future_to_load = {executor.submit(loading_images, file_index, output_folder): file_index for file_index in np.arange(0, 10)}
    for future in concurrent.futures.as_completed(future_to_load):
        index = future_to_load[future]
        return_dict = future.result()
        global_data[return_dict['index']] = return_dict['array']

end_time = time.perf_counter()
print(f"it took {end_time - start_time}s in parallel")

        # try:
        #     data = future.result()
        # except Exception as exc:
        #     print('%r generated an exception: %s' % (url, exc))
        # else:
        #     print('%r page is %d bytes' % (url, len(data)))