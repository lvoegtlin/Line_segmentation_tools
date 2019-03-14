import os
import shutil

BASE_PATH = '/Users/voegtlil/Documents/Research/line_segmentation/results/gridSearch'

if __name__ == '__main__':
    folders = list(os.walk(BASE_PATH))[0][1]

    for folder in folders:
        subfolders = list(os.walk(os.path.join(BASE_PATH, folder)))[0][1]
        for subfolder in subfolders:
            shutil.rmtree(os.path.join(BASE_PATH, folder, subfolder))

    print('Finished cleanup!')
