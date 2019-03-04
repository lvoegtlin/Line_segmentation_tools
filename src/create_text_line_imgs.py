import os
import cv2
import numpy as np

from src.execute_on_DS import load_files

BASE_FOLDER = '/Users/voegtlil/Documents/Datasets/003-DataSet/hisdoc_DS'
PXL_BASE_FOLDER = os.path.join(BASE_FOLDER, "pxl_gt")
OUTPUT_PATH = os.path.join(BASE_FOLDER, "textline_gt")

img_list, _ = load_files()

for img_path in img_list:
    # read in image
    img = cv2.imread(os.path.join(PXL_BASE_FOLDER, img_path))

    # prepare
    # Erase green just in case
    img[:, :, 1] = 0
    # Find and remove boundaries (set to bg)
    locations = np.where(img == 128)
    img[locations[0], locations[1]] = 0
    # Find regular text and text + decoration
    locations_text = np.where(img == 8)
    locations_text_comment = np.where(img == 12)
    # Wipe the image
    img[:, :, :] = 0
    # Set the text to be white
    img[locations_text[0], locations_text[1]] = 255
    img[locations_text_comment[0], locations_text_comment[1]] = 255

    # save
    cv2.imwrite(os.path.join(OUTPUT_PATH, img_path), img)
