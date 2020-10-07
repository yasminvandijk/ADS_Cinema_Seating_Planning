import pandas as pd
from os import listdir
from os.path import isfile, join
import numpy as np
import subprocess
import time

TEST_DIR = 'TestCases/'
ALGORITHM_DIR = 'python_algorithms/'

if __name__ == '__main__':

    for algorithm in listdir(ALGORITHM_DIR):
        if '.py' in algorithm and 'ilp' not in algorithm:
            dataframe = pd.DataFrame(columns = ['test_instance', 'nr_people_seated', 'nr_unavailable_places', 'running_time'])
            print(f'running {algorithm[:-3]}')

            for f in listdir(TEST_DIR):
                if isfile(join(TEST_DIR, f)):
                    with open(join(TEST_DIR, f)) as file:
                        if ('online' in algorithm and 'Online' in f) or ('offline' in algorithm and 'Exact' in f):
                            try:
                                print(f'\t with test case {f[:-4]}')
                                start = time.time()
                                output = subprocess.check_output(['python3', join(ALGORITHM_DIR, algorithm)], stdin=file)
                                end = time.time()
                                output = output.split()

                                if output[0] == -1:
                                   dataframe = dataframe.append({'test_instance': f[:-4], 'nr_people_seated': 'N\A', 'nr_unavailable_places': 'N\A', 'running_time': 'N\A'}, ignore_index = True)
                                else:
                                    dataframe = dataframe.append({'test_instance': f[:-4], 'nr_people_seated': output[0], 'nr_unavailable_places': output[1], 'running_time': end - start}, ignore_index = True)

                                print(dataframe)
                            except KeyboardInterrupt:
                                dataframe = dataframe.append({'test_instance': f[:-4], 'nr_people_seated': 'N\A', 'nr_unavailable_places': 'N\A', 'running_time': 'N\A'}, ignore_index = True)
                                pass

            dataframe.to_csv(algorithm[:-3] + '.csv')
            
    #             print(f)
    #             nrRows = int(file.readline())
    #             nrCols = int(file.readline())
    #             print(nrRows, nrCols)

    #             # cinema layout
    #             layout = np.empty((nrRows, nrCols), dtype = str)
    #             for i in range(nrRows):
    #                 layout[i] = [b for b in file.readline().strip()]

    #             if 'Exact' in f:
    #             # number of groups for each group size
    #                 nrGroupsTotal = np.array([int(nr) for nr in file.readline().split()])

    #                 nrTotalPeople = 0
    #                 for i in range(len(nrGroupsTotal)):
    #                     nrTotalPeople += (i + 1) * nrGroupsTotal[i]
                    
    #             else:
    #                 nrTotalPeople = 0
    #                 nr = file.readline().strip()
    #                 while nr != '0':
    #                     print(nr)
    #                     nrTotalPeople += int(nr)
    #                     nr = file.readline().strip()

    
