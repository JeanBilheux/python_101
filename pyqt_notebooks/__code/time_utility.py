import os
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
import time


def format_time_stamp(file_name = None, time_stamp = None):
    """Format the time stamp to easily retrieve the day, time, hour,
    and keep only short file name"""
    
    _short_file_name = os.path.basename(file_name)
    [week_day, month, day, hours, year] = time_stamp.split()
    
    [hours, minutes, seconds] = hours.split(':')
    _dict_time = {"hours": hours,
                  "minutes": minutes,
                  "seconds": seconds}
    
    _dict_time_stamp = {"week_day": week_day,
                       "month": month,
                       "day": day,
                       "hours": _dict_time,
                       "year": year}
    
    return [_short_file_name, _dict_time_stamp]


def retrieve_time_stamp(filename=''):
    if not os.path.exists(filename):
        return -1
    
    image = Image.open(filename)
    metadata = image.tag_v2.as_dict()
    acquisition_time = metadata[65000][0]
    
    time_stamp = {}
    time_stamp['acquisition_time_computer_format'] = acquisition_time
    time_stamp['acquisition_time_user_format'] = time.ctime(acquisition_time)
    
    return time_stamp

def retrieve_exposure_time(filename=''):
    if not os.path.exists(filename):
        return -1
    
    image = Image.open(filename)
    metadata = image.tag_v2.as_dict()

    exposure_label_and_time = metadata[65021][0].split(':')
    exposure_time = np.float(exposure_label_and_time[1])
    
    return exposure_time