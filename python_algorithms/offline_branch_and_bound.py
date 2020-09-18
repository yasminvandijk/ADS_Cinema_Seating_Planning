# branch and bound: (https://www.geeksforgeeks.org/8-puzzle-problem-using-branch-and-bound/)
# priority queue (https://docs.python.org/3/library/queue.html#queue.PriorityQueue)

import numpy as np
from queue import PriorityQueue
import copy

class Cinema(object):
    def __init__(self, nrRows: int, nrCols: int, layout: np.array):
        self.nrRows = nrRows
        self.nrCols = nrCols
        self.layout = layout
        self.totalPlaced = 0
        self.totalUnavailablePlaces = 0

    def printCinema(self):
        """
        prints the cinema to the terminal
        '0' for no seat, '1' for an available seat,
        'x' for an occupied seat, '+' for an unavailable seat
        """
        print()
        for row in self.layout:
            print(''.join(row))
        print()

    def printOutput(self):
        """
        prints the cinema to the terminal in the output specified as in the assignment
        '0' for no seat, '1' for a seat that is not occupied
        'x' for an occupied seat
        """
        print()
        for row in self.layout:
            rowStr = ''
            for i in range(self.nrCols):
                if (row[i] == '+'):
                    rowStr = rowStr + '1'
                else:
                    rowStr = rowStr + row[i]
            print(rowStr)
        print()
    
    def ratio(self) -> float:
        if (self.totalUnavailablePlaces == 0):
            return 0

        return self.totalPlaced / self.totalUnavailablePlaces
        
    def getAvailableSeats(self, rowIndex: int) -> [(int, int)]:
        """
        returns a list of groups of adjacent available seats
        as tuples of the start index and the number of seats
        [(startindex, nrSeats), ...]
        """
        result: [(int, int)] = []

        colIndex: int = 0

        while (colIndex < self.nrCols):
            nrSeats: int = 0
            startIndex: int = colIndex
            
            while (colIndex < nrCols and self.layout[rowIndex, colIndex] == '1'):
                colIndex = colIndex + 1
                nrSeats = nrSeats + 1

            if (nrSeats > 0):
                result.append((startIndex, nrSeats))
            colIndex = colIndex + 1
        
        return result
    
    def markUnavailable(self, rowIndex: int, colIndex: int) -> int:
        """
        sets an empty, available seat ('1') to an unavailable seat ('+')
        doesn't check indexes for array bounds
        return 1 if a seat becomes unavailable, 0 otherwise
        """
        if (self.layout[rowIndex, colIndex] == '1'):
            self.layout[rowIndex, colIndex] = '+'
            return 1
        return 0
    
    def placeGroup(self, rowIndex: int, colIndex: int, groupSize: int) -> None:
        """
        set occupied seats to 'x' and seats that have become unavailable to '+'
        """
        # mark occupied seats
        for i in range(groupSize):
            self.layout[rowIndex, colIndex + i] = 'x'

        # unavailable seats - one row above
        if (rowIndex > 0):
            for i in range(groupSize):
                self.totalUnavailablePlaces += self.markUnavailable(rowIndex - 1, colIndex + i)
            if (colIndex > 0):
                self.totalUnavailablePlaces += self.markUnavailable(rowIndex - 1, colIndex - 1)
            if (colIndex + groupSize < self.nrCols):
                self.totalUnavailablePlaces += self.markUnavailable(rowIndex - 1, colIndex + groupSize)
        
        # unavailable seats - one row underneath
        if (rowIndex + 1 < self.nrRows):
            for i in range(groupSize):
                self.totalUnavailablePlaces += self.markUnavailable(rowIndex + 1, colIndex + i)
            if (colIndex > 0):
                self.totalUnavailablePlaces += self.markUnavailable(rowIndex + 1, colIndex - 1)
            if (colIndex + groupSize < self.nrCols):
                self.totalUnavailablePlaces += self.markUnavailable(rowIndex + 1, colIndex + groupSize)

        # unavailable seats - left and right sides (2 seats each)
        if (colIndex > 0):
            self.totalUnavailablePlaces += self.markUnavailable(rowIndex, colIndex - 1)
        if (colIndex > 1):
            self.totalUnavailablePlaces += self.markUnavailable(rowIndex, colIndex - 2)
        if (colIndex + groupSize < self.nrCols):
            self.totalUnavailablePlaces += self.markUnavailable(rowIndex, colIndex + groupSize)
        if (colIndex + groupSize + 1 < self.nrCols):
            self.totalUnavailablePlaces += self.markUnavailable(rowIndex, colIndex + groupSize + 1)
    
    def findSeating(self, groupSize) -> bool:
        """
        iteratively check each row until a row is found where this group fits
        places the group on that row as far to the left as possible
        returns true if group is placed, false otherwise
        """
        # check if group is smaller or equal to number of columns
        if (groupSize > self.nrCols):
            return False
        
        # check for each row if group fits
        for y in range(nrRows):
            availableSeats = [x for x in self.getAvailableSeats(y) if x[1] >= groupSize]
            if (len(availableSeats) > 0):
                # a possible seating is found, take the first seating and place group there
                seating: (int, int) = availableSeats[0]
                self.placeGroup(y, seating[0], groupSize)
                self.totalPlaced = groupSize

                return True
                #self.printCinema()

        return False

def solve(cinema: Cinema, nrGroupsTotal: np.array):
    queue = PriorityQueue()
    queue.put((0, (cinema, nrGroupsTotal)))

    bestRatio: float = None
    bestCinema: Cinema = None

    while not queue.empty():
        _, (partialSolution, groups) = queue.get()

        for groupIndex in range(len(groups)):
            if groups[groupIndex] > 0:
                print(f'group of {groupIndex + 1}')
                newCinema = copy.deepcopy(partialSolution)
                if newCinema.findSeating(groupIndex + 1):
                    groupsRemaining = copy.deepcopy(groups)
                    groupsRemaining[groupIndex] -= 1

                    ratio: float = newCinema.ratio()
                    print(ratio)
                    newCinema.printCinema()

                    if bestRatio is None or ratio > bestRatio:
                        print('better ratio')
                        bestRatio = ratio
                        bestCinema = copy.deepcopy(newCinema)
                        queue.put((bestRatio, (copy.deepcopy(newCinema), copy.deepcopy(groupsRemaining))))
                        # bestCinema.printCinema()

        # loop over groupsizes
        # create new partial solutions
        # check whether it should be bound or added to queue

    return bestCinema
        


if __name__ == '__main__':
    # number of rows and columns
    nrRows = int(input())
    nrCols = int(input())

    # cinema layout
    layout = np.empty((nrRows, nrCols), dtype = str)
    for i in range(nrRows):
        layout[i] = [b for b in input()]

    # number of groups for each group size
    nrGroupsTotal = np.array([int(nr) for nr in input().split()])

    # number of groups placed for each group size
    nrGroupsPlaced = np.full((len(nrGroupsTotal)), 0, dtype=int)

    cinema = Cinema(nrRows, nrCols, layout)

    # loop over groups in descending group size
    bestCinema = solve(cinema, nrGroupsTotal)

    # output
    bestCinema.printOutput()
    
    # print some extra info
    bestCinema.printCinema()
    print(f'groups: {nrGroupsTotal}')
    print(f'placed: {nrGroupsPlaced}')

    totalVisitors: int = 0

    for i in range(len(nrGroupsTotal)):
        totalVisitors = totalVisitors + nrGroupsTotal[i] * (i + 1)
    
    print(f'placed: {bestCinema.totalPlaced} out of {totalVisitors}')
