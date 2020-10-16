import matplotlib.pyplot as plt
import pandas as pd
import os
from mpl_toolkits.mplot3d import axes3d

RESULTS_DIR = 'C#_algorithms/ADS_CinemaSeating/ADS_CinemaSeating/Test_Results/'
TEST_INSTANCES_DATA = 'test_instances_data.csv'
CASES = ['Offline/', 'Online/']


if __name__ == '__main__':
    df_test_instances = pd.read_csv(TEST_INSTANCES_DATA).sort_values(by = 'testcase')

    legend = []
    for case in CASES:
        for filename in os.listdir(RESULTS_DIR + case):
            df_result = pd.read_csv(RESULTS_DIR + case + filename)
            df_merged = df_result.merge(df_test_instances)
            df_merged['ratio_people_seated'] = df_merged[' nr_occupied_seats'] / df_merged['nr_coming_people'] * 100.
            df_merged['ratio_occupied_seats'] = df_merged[' nr_occupied_seats'] / df_merged['nr_seats'] * 100.
            # print(df_merged)
            # fig = plt.figure()
            # ax = plt.axes(projection="3d")
            # ax.plot3D()

            if filename == 'online_first_fit.csv' or filename == 'offline_best_fit_big_first.csv':
                legend.append(filename[:-4])
                print(legend)
                plt.plot(df_merged['nr_coming_people'], df_merged['ratio_people_seated'])

    plt.xlabel('Number of Total People')
    plt.ylabel('Ratio of People Seated (%)')
    plt.title('Ratio of Seat Occupation for best Online and Offline Algorithms')    
    plt.legend(legend)
    plt.show()
            # print(df_merged)