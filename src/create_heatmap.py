import csv
import os
import numpy as np
import matplotlib.pyplot as plt

from natsort import natsorted

BASE_PATH = '/Users/voegtlil/Documents/Research/line_segmentation/results/gridSearch'


def get_params(name):
    split = name.split('_')

    return int(split[2]), int(split[4])


def get_avg_score(path):
    with open(os.path.join(path, 'summary.csv'), 'r') as file:
        reader = csv.reader(file)
        return np.average([float(line[5]) for i, line in enumerate(list(reader)) if i != 0])


if __name__ == '__main__':
    penalties = list(range(2000, 13000, 1000))
    seams_per = list(range(10, 110, 10))

    scores = []

    # iteratoe throw all folders
    folders = list(os.walk(BASE_PATH))[0][1]
    folders = natsorted(folders)

    current_penalty = 2000
    penalty_score = []

    for folder in folders:
        penalty, seam = get_params(folder)
        score = get_avg_score(os.path.join(BASE_PATH, folder))
        scores.append(score)
        # if penalty != current_penalty:
        #     scores.append(penalty_score)
        #     penalty_score = []
        #     current_penalty = penalty
        # else:
        #     penalty_score.append(score)

    penalties = np.asarray(penalties)
    seams_per = np.asarray(seams_per)
    scores = np.asarray(scores)
    scores = scores.reshape((11, 10))

    # feed them to mathplotlibfig,
    fig, ax = plt.subplots()
    im = ax.imshow(scores, cmap="YlGn")

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('', rotation=-90, va="bottom")

    ax.set_xticks(np.arange(len(seams_per)))
    ax.set_yticks(np.arange(len(penalties)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(seams_per)
    ax.set_yticklabels(penalties)

    ax.set_ylabel('Penalty ' + r'$\alpha$')
    ax.set_xlabel('Seam every ' + r'$\beta$' + ' pixel')

    ax.set_title("Parameter Robustness Evaluation - line IU")

    plt.savefig(os.path.join(BASE_PATH, 'grid_search_heatmap.png'))


