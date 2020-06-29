import cv2
import numpy as np
import os

# left_image = 'data/left_image.tif'
# right_image = 'data/right_image.tif'
# assert os.path.exists(left_image)
# assert os.path.exists(right_image)
# top = cv2.imread(left_image, cv2.IMREAD_UNCHANGED)
# bottom = cv2.imread(right_image, cv2.IMREAD_UNCHANGED)

# https://www.youtube.com/watch?v=ToldvnUtBh0
left_jpg = 'data/left_image.jpg'
right_jpg = 'data/right_image.jpg'
assert os.path.exists(left_jpg)
assert os.path.exists(right_jpg)
left = cv2.imread(left_jpg, cv2.IMREAD_UNCHANGED)
right = cv2.imread(right_jpg, cv2.IMREAD_UNCHANGED)

sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(left, None)
kp2, des2 = sift.detectAndCompute(right, None)

# cv2.imshow('original_image_left_keypoints', cv2.drawKeypoints(left, kp1, None))
# cv2.waitKey()

match = cv2.BFMatcher()
matches = match.knnMatch(des1, des2, k=2)

good = []
for m, n in matches:
	if m.distance < 0.03*n.distance:
		good.append(m)

draw_parameters = dict(matchColor=(0, 255, 0),
                       singlePointColor=None,
                       flags=2)

img3 = cv2.drawMatches(left, kp1, right, kp2, good, None, **draw_parameters)
cv2.imwrite('original_image_drawMaches.jpg', img3)

## not working with our data !!!
