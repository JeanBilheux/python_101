import glob
import os
import numpy as np
from pystackreg import StackReg
from skimage import io
from tqdm import tqdm
from PIL import Image
import sys, getopt
from datetime import datetime


def main(argv):

    start = datetime.now()

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

    list_files = glob.glob(os.path.join(input_folder, "*.tiff"))
    assert len(list_files) > 0

    print("Loading the data ... ", end=" ")
    list_images = []
    for _file in tqdm(list_files):
        list_images.append(io.imread(_file))
    print("Done!")

    print("converting to np array ...", end=" ")
    list_images_3d_array = np.asarray(list_images)
    print("Done!")

    print("Starting registration ...", end=" ")
    sr = StackReg(StackReg.RIGID_BODY)
    out_first = sr.register_transform_stack(list_images_3d_array, reference='first')
    print("Done!")

    print("Exporting ... ", end=" ")

    if output_folder == "":
        input_base_folder_name = os.path.basename(os.path.abspath(input_folder))
        input_folder_name = os.path.dirname(os.path.abspath(input_folder))
        output_folder_name = os.path.join(input_folder_name, input_base_folder_name + "_registered")
    else:
        output_folder_name = output_folder

    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)

    for _index in tqdm(np.arange(len(list_files))):
        filename = list_files[_index]
        base_name = os.path.basename(filename)
        output_filename = os.path.join(output_folder_name, base_name)
        im = Image.fromarray(out_first[_index])
        im.save(output_filename)
    print("Done exporting!")
    print(f"data exported to {output_filename}")

    finish = datetime.now()

    print(f"It took {finish - start}s to process {len(list_files)} images!")


if __name__ =="__main__":
    main(sys.argv[1:])
