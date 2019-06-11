import cv2
import os
import numpy as np

import xml.etree.ElementTree as ET


# FOLDER_NAME_EXTENSION = '_penalty_reduction_90_seams_3000'


def get_file_list(dir):
    list = []
    for root, _, fnames in sorted(os.walk(dir)):
        for fname in fnames:
            path = os.path.join(root, fname)
            list.append(path)
    list.sort()
    return list


def get_polygons(xml_path):
    # load xml
    tree = ET.parse(xml_path)
    root = tree.getroot()
    # get all textlines
    text_lines = root.find('Page').findall('.//TextLine')
    print('Amount of lines: ' + str(len(text_lines)))

    polygons = []
    for textLine in text_lines:
        coord_string = textLine.find('Coords').attrib['points']
        coord_string = coord_string.split(' ')
        polygons.append([[int(coord.split(',')[0]), int(coord.split(',')[1])] for coord in coord_string])

    # return list of points
    return polygons


def draw_polygons(image, polygons):
    overlay_img = image.copy()
    for i, polygon in enumerate(polygons):
        cv2.polylines(image, np.array([[[np.int(p[0]), np.int(p[1])] for p in polygon]]), 1, color=((i*64) % 255, (i*32) % 255, (i*128)% 255), thickness=3)
        # cv2.fillPoly(overlay_img, np.array([[[np.int(p[0]), np.int(p[1])] for p in polygon]]), color=(0, 128, 0))
    cv2.addWeighted(overlay_img, 0.4, image, 0.6, 0, image)
    return image


def overlay(path_img, path_xml, output_path):
    # load image
    img = cv2.imread(path_img)

    # parse out the polygons
    polygons = get_polygons(path_xml)

    # overlay polygon with image
    cv2.imwrite(output_path, draw_polygons(img, polygons))


if __name__ == '__main__':
    # get folders in the output folder
    # images = ['lines']

    input_folder = "/Users/voegtlil/Documents/09_Papers/HIPS 19/images/overlay"
    overlay(os.path.join(input_folder, "00012-42.JPG"),
            os.path.join(input_folder, "polygons.xml"),
            os.path.join(input_folder, "overlay.jpg")
            )

    # # folders
    # xml_root = './../../res/new_image'
    #
    # for img in images:
    #     # get xmls
    #     overlay('./../../res/new_image/' + img +'.png',
    #             os.path.join(xml_root, 'polygons.xml'),
    #             os.path.join(xml_root, 'overlay.jpg'))
