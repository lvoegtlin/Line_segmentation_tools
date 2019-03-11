import csv
import os


def get_csv_content():
    # read csv
    with open('/Users/voegtlil/Downloads/experiment_65871_observations.csv', 'r') as file:
        reader = csv.reader(file)
        return list(reader)[1:]


if __name__ == '__main__':
    lines = get_csv_content()

    for line in lines:
        path_base_folder = '/Users/voegtlil/Downloads/penalty_reduction_{}_seams_{}'.format(line[0], line[1])
        # create folder
        os.mkdir(path_base_folder)

        with open(os.path.join(path_base_folder, 'summary.csv'), 'w') as file:
            # fill first line in case of beeing the first csv
            file.write('filename,filename,NbLinesTruth,NbLinesProposed,NbLinesCorrect,LinesIU,LinesFMeasure,'
                       'LinesRecall,LinesPrecision,MatchedPixelIU,MatchedPixelFMeasure,MatchedPixelPrecision,'
                       'MatchedPixelRecall,PixelIU,PixelFMeasure,PixelPrecision,PixelRecall\n')
            file.write('A,B,C,D,E,{},G,H,I,J,K,L,M,N,O,P,Q'.format(line[2]))

