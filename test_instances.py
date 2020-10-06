import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np

TEST_DIRECTORY = 'TestCases/'

if __name__ == '__main__':
    dataframe = pd.DataFrame(columns = ['test_instance', 'cinema_size', 'nr_seats', 'nr_coming_people'])

    for f in listdir(TEST_DIRECTORY):
        if isfile(join(TEST_DIRECTORY, f)):
            with open(join(TEST_DIRECTORY, f)) as file:
                print(f)
                nrRows = int(file.readline())
                nrCols = int(file.readline())
                print(nrRows, nrCols)

                # cinema layout
                layout = np.empty((nrRows, nrCols), dtype = str)
                for i in range(nrRows):
                    layout[i] = [b for b in file.readline().strip()]

                nrGroupsTotal = np.array([int(nr) for nr in file.readline().split()])
                if 'Exact' in f:
                # number of groups for each group size

                    nrTotalPeople = 0
                    for i in range(len(nrGroupsTotal)):
                        nrTotalPeople += (i + 1) * nrGroupsTotal[i]
                    
                else:
                    nrTotalPeople = 0
                    for i in range(len(nrGroupsTotal)):
                        nrTotalPeople += nrGroupsTotal[i]

                dataframe = dataframe.append({'test_instance': f[:-4], 'cinema_size': nrRows * nrCols, 'nr_seats': np.count_nonzero(layout == '1'), 'nr_coming_people': nrTotalPeople}, ignore_index = True)
    
    dataframe.to_csv('test_instances_data.csv')
