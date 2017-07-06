import numpy as np
from scipy.ndimage import convolve


def gamma_filtering(data_array, threshold=0.1):
    
    final_data_array = []
    for _data in data_array:
        _data_filtered = single_gamma_filtering(_data)
        final_data_array.append(_data_filtered)
        
    return final_data_array 


def single_gamma_filtering(data, threshold=0.1):
    
    raw_data = np.copy(data)
    
    # find mean counts
    mean_counts = np.mean(raw_data)
    
    thresolded_raw_data = raw_data * threshold
    
    # get pixels where value is above threshold
    position = []
    [height, width] = np.shape(raw_data)
    for _x in np.arange(width):
        for _y in np.arange(height):
            if thresolded_raw_data[_y, _x] > mean_counts:
                position.append([_y, _x])
                
    # convolve entire image using 3x3 kerne
    mean_kernel = np.array([[1,1,1], [1,0,1], [1,1,1]]) / 8.0
    convolved_data = convolve(raw_data, mean_kernel, mode='constant')
    
    # replace only pixel above threshold by convolved data
    for _coordinates in position:
        [_y, _x] = _coordinates
        raw_data[_y, _x] = convolved_data[_y, _x]
        
    return raw_data

def local_gamma_filtering(coeff=0.5, grid_size=3, image=[]):
    '''
    if 0.5 * count of pixel is > mean of grid size 
    
    grid_size must be odd number
    '''
    
    if grid_size % 2 == 0:
        raise ValueError("Grid size must be an odd nmber")
    
    [image_height, image_width] = np.shape(image)    
    
    offset = np.int(grid_size/2)
    
    clean_image = np.array(image, dtype=float)
    for _h in np.arange(offset, image_height-1-offset):
        for _w in np.arange(offset, image_width-1-offset):
            _grid_array = np.array(image[_h-offset:_h+offset+1, _w-offset:_w+offset+1], dtype=float)
            _grid_array[offset, offset] = np.NaN
            _mean_value = np.nanmean(_grid_array)
            
            pixel_value = image[_h, _w]
            
            if coeff * pixel_value > _mean_value: #gamma
                clean_image[_h, _w] = _mean_value
            else:
                clean_image[_h, _w] = pixel_value
                
    return clean_image  

def scipy_gamma_filtering(data=[], threshold=0.2):
    
 #This function finds the hot or dead pixels in a 2D dataset. 
    #tolerance is the number of standard deviations used to cutoff the hot pixel
    #
    #The function returns a list of hot pixels and also an image with with hot pixels removed

    from scipy.ndimage import median_filter
    blurred = median_filter(data, size=2)
    difference = data - blurred

    #find the hot pixels, but ignore the edges
    hot_pixels = np.nonzero((np.abs(difference[1:-1,1:-1])>threshold) )
    hot_pixels = np.array(hot_pixels) + 1 #because we ignored the first row and first column

    fixed_image = np.copy(data) #This is the image with the hot pixels removed
    for y,x in zip(hot_pixels[0],hot_pixels[1]):
        fixed_image[y,x]=blurred[y,x]
   
    return fixed_image
