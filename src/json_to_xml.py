# read in json
import fnmatch
import json
import os
import xml.etree.ElementTree as ET

from src.XMLhandler import writePAGEfile

BASE_FOLDER = './../res/on_gt_full_page'
JSON_BASE_FOLDER = os.path.join(BASE_FOLDER, "pxl_gt")
OUTPUT_PATH = os.path.join(BASE_FOLDER, "textline_output")


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
    for the_file in os.listdir(folder):
        if fnmatch.fnmatch(the_file, '*.xml'):
            return os.path.join(folder, the_file)
    return None


def get_offset(folder):
    xml_path = get_xml_path(folder)
    if xml_path is None:
        return
    tree = ET.parse(xml_path)
    root = tree.getroot()

    return root[1][0][0].attrib['points'].split(" ")[0]


folders = get_folder_list(BASE_FOLDER)

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
        if data is None:
            continue
        for polygon in data:
            line_string = []
            # bring it into string format
            for i, point in enumerate(polygon['array']['values']):
                if i % 3 != 0:
                    continue
                line_string.append("{},{}".format(int(point[1]), int(point[0])))
            strings.append(' '.join(line_string))
    # write down the xml
    writePAGEfile(output_path=os.path.join(folder, "polygons.xml"), text_lines=strings)
