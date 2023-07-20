import glob
import os
import numpy as np
from pystackreg import StackReg
from skimage import io

input_folder = "/HFIR/CG1D/IPTS-30750/shared/processed_data/normalized/cropped/23_06_09_left/"
assert os.path.exists(input_folder)

list_files = glob.glob(os.path.join(input_folder, "*.tiff"))
assert len(list_files) > 0

list_images = []
for _file in list_files:
    list_images.append(io.imread(_file))

list_images_3d_array = np.asarray(list_images)

print("Starting registration ...")

sr = StackReg(StackReg.RIGID_BODY)
out_first = sr.register_transform_stack(list_images_3d_array, reference='first')

print("Done !")