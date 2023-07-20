import glob
import os
import numpy as np
from pystackreg import StackReg
from skimage import io
from tqdm import tqdm
from PIL import Image


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

print("Exporting")

input_base_folder_name = os.path.basename(input_folder)
input_folder_name = os.path.dirname(input_folder)

output_folder_name = os.path.join(input_folder_name, input_base_folder_name + "_registered")

for _index in tqdm(np.arange(len(list_files))):
    filename = list_files[_index]
    base_name = os.path.basename(filename)
    output_filename = os.path.join(output_folder_name, base_name)
    im = Image.fromarray(out_first[_index])
    im.save(output_filename)

print("Done exporting!")
