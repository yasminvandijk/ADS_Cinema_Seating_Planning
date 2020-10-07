# branch and bound: (https://www.geeksforgeeks.org/8-puzzle-problem-using-branch-and-bound/)
# priority queue (https://docs.python.org/3/library/queue.html#queue.PriorityQueue)

"""
branch and bound strategy:
start with an empty cinema and all groups that still need to be placed, this is the first 
partial solution with a priority score equal to it's total number of available seats
put this partial solution on a priority queue sorted on descending priority score

create new partial solutions by taking the first item of the priority queue and looping 
over all the groupsizes for which groups still need to be placed
for each groupsize; add a new partial solution with a group of that size placed 
(at a bruted forced best place?),
and a priority score equal to the total number of people placed so far 
plus the total number of remaining available seats

keep track of the best solution so far, by checking the total number of people placed so far
bound partial solutions by checking if the total number of people placed plus the total number 
of remaining available places is less than the maximum number of people placed in the best 
solution we have found so far
if this is the case, this solution can not be better than the best solution we have found so far
no matter how we fill the remaining available seats
this is because the maximum number of people that could be placed can not exceed the number of 
people placed so far plus the number of available remaining seats
this means we do not have to continue branching this partial solution
"""

import numpy as np
import copy
from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any
import time

TIMELIMIT = 1800

class Cinema(object):
    def __init__(self, nrRows: int, nrCols: int, layout: np.array):
        self.nrRows = nrRows
        self.nrCols = nrCols
        self.layout = layout
        self.totalPlaced = 0
        self.totalRemainingPlaces = self.countRemainingSeats()
        self.seatList = []  # 1: [(1, 1), (2, 2), ...]
        self.initSeatList()
    

    def initSeatList(self):
        for row in range(self.nrRows):
            self.seatList.append(dict())
            self.updateRowSeatList(row)


    def updateRowSeatList(self, rowIndex: int):
        availableSeats = self.getAvailableSeats(rowIndex)
        self.seatList[rowIndex] = dict()

        for seat in availableSeats:
            print(seat)
            if seat[1] in self.seatList[rowIndex]:
                self.seatList[rowIndex][seat[1]].append(seat[0])
            else:
                self.seatList[rowIndex][seat[1]] = [seat[0]]
    

    def updateRowsSeatList(self, rowIndex: int):
        if rowIndex > 0:
            self.updateRowSeatList(rowIndex - 1)

        self.updateRowSeatList(rowIndex)

        if rowIndex < self.nrRows - 1:
            self.updateRowSeatList(rowIndex + 1)


    def countUnavailableSeats(self, rowIndex: int, colIndex: int, groupSize: int, nrSeats: int) -> (int, int):
        lowestCount = None
        bestColIndex = None
        for column in range(colIndex, colIndex + nrSeats - groupSize + 1):
            count = 0
            if (rowIndex > 0):
                for i in range(groupSize):
                    count += 1
                if (column > 0):
                    count += 1
                if (column + groupSize < self.nrCols):
                    count += 1
            
            # unavailable seats - one row underneath
            if (rowIndex + 1 < self.nrRows):
                for i in range(groupSize):
                    count += 1
                if (column > 0):
                    count += 1
                if (column + groupSize < self.nrCols):
                    count += 1

            # unavailable seats - left and right sides (2 seats each)
            if (column > 0):
                count += 1
            if (column > 1):
                count += 1
            if (column + groupSize < self.nrCols):
                count += 1
            if (column + groupSize + 1 < self.nrCols):
                count += 1

            if lowestCount is None or count < lowestCount:
                lowestCount = count
                bestColIndex = column

        return (lowestCount, bestColIndex)


    def countRemainingSeats(self) -> int:
        """
        returns the total number of remaining available seats;
        the total number of seats marked as '1'
        """
        result: int = 0
        for row in self.layout:
            for seat in row:
                if (seat == '1'):
                    result += 1
        return result
    
    def printCinema(self) -> None:
        """
        prints the cinema to the terminal
        '0' for no seat, '1' for an available seat,
        'x' for an occupied seat, '+' for an unavailable seat
        """
        print()
        for row in self.layout:
            print(''.join(row))
        print()

    def printOutput(self) -> None:
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
                    rowStr += '1'
                else:
                    rowStr += row[i]
            print(rowStr)
        print()
    
    def score(self) -> int:
        """
        returns the total number of people placed plus the total number of remaining available seats
        this score is used as an upper bound; the total number of people placed can not exceed this score
        if already placed groups remain seated and only new groups get placed
        """
        return self.totalPlaced + self.totalRemainingPlaces
        
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
    
    def markUnavailable(self, rowIndex: int, colIndex: int) -> None:
        """
        sets an empty, available seat ('1') to an unavailable seat ('+')
        warning: doesn't check indexes for array bounds;
        decrements total number of remaining available seats if a seat becomes unavailable
        """
        if (self.layout[rowIndex, colIndex] == '1'):
            self.layout[rowIndex, colIndex] = '+'
            self.totalRemainingPlaces -= 1
    
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
                self.markUnavailable(rowIndex - 1, colIndex + i)
            if (colIndex > 0):
                self.markUnavailable(rowIndex - 1, colIndex - 1)
            if (colIndex + groupSize < self.nrCols):
                self.markUnavailable(rowIndex - 1, colIndex + groupSize)
        
        # unavailable seats - one row underneath
        if (rowIndex + 1 < self.nrRows):
            for i in range(groupSize):
                self.markUnavailable(rowIndex + 1, colIndex + i)
            if (colIndex > 0):
                self.markUnavailable(rowIndex + 1, colIndex - 1)
            if (colIndex + groupSize < self.nrCols):
                self.markUnavailable(rowIndex + 1, colIndex + groupSize)

        # unavailable seats - left and right sides (2 seats each)
        if (colIndex > 0):
            self.markUnavailable(rowIndex, colIndex - 1)
        if (colIndex > 1):
            self.markUnavailable(rowIndex, colIndex - 2)
        if (colIndex + groupSize < self.nrCols):
            self.markUnavailable(rowIndex, colIndex + groupSize)
        if (colIndex + groupSize + 1 < self.nrCols):
            self.markUnavailable(rowIndex, colIndex + groupSize + 1)

    def findSeating(self, groupSize) -> bool:
        """
        iteratively check each row until a row is found where this group fits
        places the group on that row as far to the left as possible
        returns true if a the group is placed, false otherwise
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
                self.totalPlaced += groupSize
                self.totalRemainingPlaces -= groupSize
                return True

        return False

    def findBestSeating(self, groupSize: int) -> (int, int):
            """
            iteratively check each row until a row is found where this group fits
            places the group on that row as far to the left as possible
            returns (rowIndex + 1, colIndex + 1) if a the group is placed, (0, 0) otherwise
            """
            # check if group is smaller or equal to number of columns
            if (groupSize > self.nrCols):
                return (0, 0)
            
            leastUnavailableSeats: int = None
            leastUnavailableSeatsIndex: (int, int) = None

            # check for each row if group fits
            for y in range(nrRows):
                availableSeats = [x for x in self.getAvailableSeats(y) if x[1] >= groupSize]
                if (len(availableSeats) > 0):
                    # a possible seating is found, take the best seating and place group there
                    seating: (int, int) = availableSeats[0]
                    nrUnavailableSeats, colIndex = self.countUnavailableSeats(y, seating[0], groupSize, seating[1])
                    if leastUnavailableSeats is None or nrUnavailableSeats < leastUnavailableSeats:
                        leastUnavailableSeats = nrUnavailableSeats
                        leastUnavailableSeatsIndex = (y, colIndex)

            if leastUnavailableSeats is not None:
                self.placeGroup(leastUnavailableSeatsIndex[0], leastUnavailableSeatsIndex[1], groupSize)

                self.updateRowsSeatList(leastUnavailableSeatsIndex[0])
                # self.printCinema()

                self.totalPlaced += groupSize
                self.totalRemainingPlaces -= groupSize
                return (leastUnavailableSeatsIndex[0] + 1, leastUnavailableSeatsIndex[1] + 1)

            return (0, 0)

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: (Cinema, np.array)=field(compare=False)



def solve(cinema: Cinema, nrGroupsTotal: np.array) -> Cinema:
    """
    solve using branch and bound with a priority queue
    """
    # keep track of the best partial solution we have seen
    bestCinema: Cinema = copy.deepcopy(cinema)
    maxNrPlaced: int = 0
    
    # put the initial cinema as partial solution in the priority queue
    # items in the queue are sorted ascending on the cinema's score
    # we use negative score to ensure the partial solutions with the 
    # highest score are taken from the queue first
    queue = PriorityQueue()
    initialItem = PrioritizedItem(-cinema.score(), (cinema, nrGroupsTotal))
    queue.put(initialItem)
    
    start = time.time()
    while not queue.empty():
        current = time.time()
        if current - start > TIMELIMIT: # set timeout for 30min
            break
        # get a partial solution from the queue
        item = queue.get()
        partialCinema = item.item[0]
        nrGroupsRemaining = item.item[1]
        
        # loop over all group sizes
        for groupIndex in reversed(range(len(nrGroupsRemaining))):
            if (nrGroupsRemaining[groupIndex] > 0):
                # bound: check if this solution is worth expanding
                if (partialCinema.score() > maxNrPlaced):
                    # branch: create new partial solutions
                    cinemaCopy: Cinema = copy.deepcopy(partialCinema)
                    seating = cinemaCopy.findSeating(groupIndex + 1)
                    if seating:
                        # new partial solution found
                        nrGroupsRemainingCopy = copy.deepcopy(nrGroupsRemaining)
                        nrGroupsRemainingCopy[groupIndex] -= 1

                        # check if this partial solution is better than best solution seen so far
                        if (cinemaCopy.totalPlaced > maxNrPlaced):
                            bestCinema = copy.deepcopy(cinemaCopy)
                            maxNrPlaced = cinemaCopy.totalPlaced
                        
                        # add partial solution to priority queue
                        newPartialSolution = PrioritizedItem(-cinemaCopy.score(), (cinemaCopy, nrGroupsRemainingCopy))
                        queue.put(newPartialSolution)

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

    cinema = Cinema(nrRows, nrCols, layout)

    bestSolution = solve(cinema, nrGroupsTotal)

    # bestSolution.printCinema()

    totalVisitors: int = 0
    for i in range(len(nrGroupsTotal)):
        totalVisitors += nrGroupsTotal[i] * (i + 1)
    
    # print(f'placed: {bestSolution.totalPlaced} out of {totalVisitors}')
    print(bestSolution.totalPlaced)
    print(np.count_nonzero(bestSolution.layout == '+'))