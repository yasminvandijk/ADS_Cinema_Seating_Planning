import pandas as pd
from os import listdir
from pathlib import Path
import numpy as np
import subprocess
import time
import random
import shutil

#TEST_DIR = 'TestCases/'
#ALGORITHM_DIR = 'python_algorithms/'

def randomGuests():
    """
    docstring
    """
    randguest = random.random()
    if randguest < 0.2: return 1
    elif randguest < 0.4: return 2
    elif randguest < 0.6: return 3
    elif randguest < 0.7: return 4
    elif randguest < 0.8: return 5
    elif randguest < 0.9: return 6
    elif randguest < 0.95: return 7
    elif randguest < 1: return 8
    

def main():
    file = open("copy.txt", "w") 
    randguests = []
    for x in range(0, random.randint(200,300)):
        randguests.append(randomGuests())
    offlist = [0,0,0,0,0,0,0,0]
    for i in randguests:
        offlist[i-1] += 1
        print(i)
        file.write(str(i)+"\n") 
    offliststr = map(str,offlist)
    print(" ".join(offliststr))
    file.close() 


if __name__ == '__main__':
    main()
