# read in json
import fnmatch
import json
import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET

from src.util.XMLhandler import writePAGEfile

BASE_FOLDER_EXTRACTION = './../res/on_rgb_with_crop'
JSON_BASE_FOLDER = os.path.join(BASE_FOLDER_EXTRACTION, "pxl_gt")
OUTPUT_PATH = os.path.join(BASE_FOLDER_EXTRACTION, "textline_output")

BASE_FOLDER_XML_GT = '/Users/voegtlil/Documents/Datasets/003-DataSet/hisdoc_DS/xml_gt'

visualize = False


# get all the folders
def get_folder_list(dir):
    list = []
    for the_file in os.listdir(dir):
        file_path = os.path.join(dir, the_file)
        try:
            if os.path.isdir(file_path):
                list.append(file_path)
        except Exception as e:
            print(e)
    return list


def get_json_path(folder):
    for the_file in os.listdir(folder):
        if fnmatch.fnmatch(the_file, '*.json'):
            return os.path.join(folder, the_file)
    return None


def get_xml_path(folder):
    """ADAPT FOR NORMAL RGB (delete _gt)"""
    xml_file_path = os.path.join(BASE_FOLDER_XML_GT, os.path.basename(folder) + "_gt.xml")
    return xml_file_path.replace('output', 'gt')


def get_offset(folder):
    xml_path = get_xml_path(folder)
    if xml_path is None:
        return
    tree = ET.parse(xml_path)
    root = tree.getroot()

    return np.asarray(root[1][0][0].attrib['points'].split(" ")[0].split(","), dtype=int)


folders = get_folder_list(BASE_FOLDER_EXTRACTION)

# produces list of polygon strings
for folder in folders:
    offset = get_offset(folder)
    json_path = get_json_path(folder)
    if json_path is None or offset is None:
        continue
    # polygon as strings
    strings = []
    # get the json in it
    with open(json_path, 'r') as f:
        data = json.load(f)
        polygons = []
        if data is None:
            continue
        for polygon in data:
            polygon_points = []
            line_string = []
            # bring it into string format
            for i, point in enumerate(polygon['array']['values']):
                line_string.append("{},{}".format(int(point[0]), int(point[1])))
                polygon_points.append([int(point[1]), int(point[0])])
            strings.append(' '.join(line_string))
            polygons.append(polygon_points)

        if visualize:
            image = cv2.imread(os.path.join(BASE_FOLDER_XML_GT.replace('xml_gt', 'ori_img'), os.path.basename(folder) + '.jpg').replace('_gt', ''))
            for polygon in polygons:
                cv2.polylines(image, np.array([[[np.int(p[1]), np.int(p[0])] for p in polygon]]), 1,
                              color=(248, 24, 148), thickness=5)
                output_folder = os.path.join('./../output', os.path.basename(folder))

                if not os.path.exists(output_folder):
                    os.mkdir(output_folder)

                cv2.imwrite(os.path.join(output_folder, 'visualization.jpg'), image)

    print("Finished saving image...")
    # write down the xml
    writePAGEfile(output_path=os.path.join(folder, "polygons.xml"), text_lines=strings)
