import argparse
import glob
from PIL import Image
import time
import numpy as np

from NeuNorm.normalization import Normalization

parser = argparse.ArgumentParser(description='Loading tiff using parallel processing')
parser.add_argument('-f', '--files', help='list of files to load')
parser.add_argument('--algo', help='algo to use to load data')

def run_processing():

    args = parser.parse_args()
    list_of_files = glob.glob(args.files)

    print(f"Loading {len(list_of_files)} files")
    data = []

    if args.algo == 'pillow':

        print("using algo pillow")
        for _file in list_of_files:
            _image = Image.open(_file)
            _data = np.asarray(_image)
            data.append(_data)

    elif args.algo == 'neunorm':

        print("using algo NeuNorm")
        o_norm = Normalization()
        o_norm.load(file=list_of_files, gamma_filter=True)
        data = o_norm.data['sample']['data']

    print(np.shape(data))

if __name__ == "__main__":
    start_time = time.time()
    run_processing()
    end_time = time.time()

    print(f"It took {end_time - start_time}s")
