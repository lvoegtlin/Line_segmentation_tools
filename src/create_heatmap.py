import csv
import os

import numpy as np
import itertools
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

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
    penalties_axis = [500] + list(range(1000, 13000, 1000))
    seams_per_axis = list(range(10, 110, 10))
    penalties = []
    seams_per = []
    points = []

    scores_old = []
    scores = []

    # iteratoe throw all folders
    folders = list(os.walk(BASE_PATH))[0][1]
    folders = natsorted(folders)

    penalty_score = []

    column = 0
    for i, folder in enumerate(folders):
        penalty, seam = get_params(folder)
        score = get_avg_score(os.path.join(BASE_PATH, folder))
        scores_old.append(score)

        points.append([seam, penalty])

        if penalty not in penalties:
            penalties.append(penalty)
            scores.append(np.asarray(penalty_score))
            penalty_score = [score]
            i = 0
        else:
            penalty_score.append(score)

        if seam not in seams_per:
            seams_per.append(seam)

        i += 1
        # if penalty != current_penalty:
        #     scores.append(penalty_score)
        #     penalty_score = []
        #     current_penalty = penalty
        # else:
        #     penalty_score.append(score)

    penalties = np.asarray(penalties)
    seams_per = np.asarray(seams_per)
    # scores = np.asarray(scores_old).reshape((13, 10)).transpose()
    scores = np.asarray(scores)

    # interpolation
    grid_z0 = griddata(points, scores_old, (np.asarray([seams_per]), penalties[:, None]), method='linear')

    # feed them to mathplotlibfig,
    fig, ax = plt.subplots()
    # im = ax.imshow(scores, cmap="YlGn")
    im = ax.imshow(grid_z0[0:35].T, cmap="YlGn")

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('line IU', rotation=-90, va="bottom")

    ax.set_yticks(np.arange(len(seams_per)))
    ax.set_xticks(np.arange(len(penalties[0:35])))
    # ... and label them with the respective list entries
    ax.set_yticklabels(seams_per)
    ax.set_xticklabels(penalties, rotation=60)

    ax.set_xlabel('Penalty ' + r'$\beta$')
    ax.set_ylabel('Seam every ' + r'$\alpha$' + ' pixel')

    ax.set_title("Parameter Robustness Evaluation")

    plt.savefig(os.path.join(BASE_PATH, 'grid_search_heatmap.png'))


