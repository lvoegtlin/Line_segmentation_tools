import os
import numpy as np

import cv2

BASE_PATH = '/Users/voegtlil/Documents/Research/line_segmentation/Paper/Images/overlay_ori_with_vis'

ORIGINAL_IMAGE = os.path.join(BASE_PATH, 'e-codices_csg-0863_004_max.jpg')
VISIALIZATION = os.path.join(BASE_PATH, 'e-codices_csg-0863_004_max_output-visualization.png')

# read original image
ori = cv2.imread(ORIGINAL_IMAGE)

# read visialization
vis = cv2.imread(VISIALIZATION)

# add the images where its not black
location = np.where(vis != 0)
ori[location] = vis[location]

cv2.imwrite(os.path.join(BASE_PATH, 'fun.png'), ori)
