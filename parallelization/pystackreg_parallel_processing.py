import concurrent.futures
import glob
import logging

import numpy as np
from PIL import Image
import time
from skimage import io
import sys
import os
import getopt
from collections import deque
from pystackreg import StackReg
import logging


LOGGER_FILENAME = os.path.abspath("~/.pystackreg.log")


def split_list(input_list, chunk_size):
    # Create a deque object from the input list
    deque_obj = deque(input_list)
    # While the deque object is not empty
    while deque_obj:
        # Pop chunk_size elements from the left side of the deque object
        # and append them to the chunk list
        chunk = []
        for _ in range(chunk_size):
            if deque_obj:
                chunk.append(deque_obj.popleft())

        # Yield the chunk
        yield chunk


def main(argv):

    logging.basicConfig(filename=LOGGER_FILENAME,
                        filemode='a',
                        format='[%(levelname)s] - %(asctime)s - %(message)s',
                        level=logging.INFO)
    logging.info("*** Starting a new registration ***")

    start_time = time.perf_counter()

    input_folder = ''
    output_folder = ''

    opts, args = getopt.getopt(argv, "hi:o:", ["ifolder=", "ofolder="])

    for opt, arg in opts:

        if opt == '-h':
            print("python pystackreg_script.py -i <input_folder> [-o <output_folder>")
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            input_folder = arg
        elif opt in ("-o", "--ofolder"):
            output_folder = arg

    # input_folder = "/HFIR/CG1D/IPTS-30750/shared/processed_data/normalized/cropped/23_06_09_left/"
    assert os.path.exists(input_folder)

    logging.info(f"input_folder: {input_folder}")
    logging.info(f"output_folder: {output_folder}")

    list_files = glob.glob(os.path.join(input_folder, "*.tiff"))
    list_files.sort()
    assert len(list_files) > 0

    logging.info(f"len(list_files): {len(list_files)}")

    if output_folder == "":
        input_base_folder_name = os.path.basename(os.path.abspath(input_folder))
        input_folder_name = os.path.dirname(os.path.abspath(input_folder))
        output_folder_name = os.path.join(input_folder_name, input_base_folder_name + "_registered")
    else:
        output_folder_name = output_folder

    logging.info(f"files will be saved in: {output_folder_name}")

    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)

    nbr_files_per_thread = 20
    list_files_per_thread = list(split_list(list_files, nbr_files_per_thread))

    # add first images to all of them
    final_list_files_per_thread = []
    for _index, _list in enumerate(list_files_per_thread):
        final_list_files_per_thread.append(_list.insert(0, list_files[0]))

    def process_images(list_filenames, output_folder):
        logging.info(f"about to process from {os.path.basename(list_filenames[1])} to {os.path.basename(list_filenames[-1])} with"
              f"reference {os.path.basename(list_filenames[0])} ")

        list_images = []
        for _file in list_filenames:
            list_images.append(io.imread(_file))

        list_images_3d_array = np.asarray(list_images)
        sr = StackReg(StackReg.RIGID_BODY)
        out_first = sr.register_transform_stack(list_images_3d_array,
                                                reference='first')

        for _index in np.arange(len(list_filenames)):
            filename = list_filenames[_index]
            base_name = os.path.basename(filename)
            output_filename = os.path.join(output_folder, base_name)
            im = Image.fromarray(out_first[_index])
            im.save(output_filename)
            logging.info(f"exporting {os.path.basename(filename)} -> {output_filename}")

        logging.info(f"Done with files from {list_images[0]} to {list_images[-1]}!")

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_load = {executor.submit(process_images, file_list, output_folder): file_list for file_list in list_files_per_thread}
        for future in concurrent.futures.as_completed(future_to_load):
            index = future_to_load[future]
            # return_dict = future.result()

    end_time = time.perf_counter()
    logging.info(f"it took {end_time - start_time}s to process the stack of data!")


if __name__ =="__main__":
    main(sys.argv[1:])
