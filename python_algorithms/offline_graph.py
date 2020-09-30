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
import networkx as nx
from networkx.algorithms import approximation


NRGROUPS = 8

class Cinema(object):
    def __init__(self, nrRows: int, nrCols: int, layout: np.array):
        self.nrRows = nrRows
        self.nrCols = nrCols
        self.layout = layout
        # nodes in the graph are tuples of (groupSize, (rowIndex, colIndex))
        self.graph = nx.Graph()
        self.layers = self._initLayers()
        self.totalPlaced = 0
        self.totalRemainingPlaces = self.countRemainingSeats()

    def _initLayers(self) -> [(int, int)]:
        layers = []
        for groupSize in range(NRGROUPS):
            seats = self.findSeating(groupSize + 1)
            for seat in seats:
                self.graph.add_node((groupSize, seat))
                # print(self.graph.nodes)
            layers.append(seats)
        
        return copy.deepcopy(layers)
        

    def createEdges(self):
        # loop through all layers and check overlap for all the nodes in the graph layers
        # print(self.graph.nodes)
        for groupSize1 in range(len(self.layers)):
            for groupSize2 in range(len(self.layers)):
                for indices1 in self.layers[groupSize1]:
                    for indices2 in self.layers[groupSize2]:
                        # if (groupSize1, indices1) != (groupSize2, indices2):
                        # if seats are on the same row, check if they're less than 2 columns apart
                        # a <= b <= c <=> a <= b && b <= c
                        if indices1[0] == indices2[0]:
                            if indices2[1] - 2 <= indices1[1] <= indices2[1] + groupSize2 + 2 and indices1[1] - 2 <= indices2[1] <= indices1[1] + groupSize1 + 2:
                                print((groupSize1 + 1, indices1), (groupSize2 + 1, indices2))
                                self.graph.add_edge((groupSize1, indices1), (groupSize2, indices2))
                                # add edge
                        # if seats are on adjacent rows, check if they're less than 1 column apart
                        elif abs(indices1[0] - indices2[0]) == 1: # don't check rows that are farther apart than 2 rows
                            if indices1[1] - 1 <= indices2[1] <= indices1[1] + groupSize1 + 1 and indices2[1] - 1 <= indices1[1] <= indices2[1] + groupSize2 + 1:
                                print((groupSize1 + 1, indices1), (groupSize2 + 1, indices2))
                                self.graph.add_edge((groupSize1, indices1), (groupSize2, indices2))
                                # add edge
                            
        # print(self.graph.edges)

    """
        (0, 0)  (0, 3)
        xx++    +++x
        +++1    x+++ (1, 0)
        1111    1111
        1111    1111
    """
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
    
    def countUnavailableSeats(self, rowIndex: int, colIndex: int, groupSize: int) -> int:
        count = 0
        if (rowIndex > 0):
            for i in range(groupSize):
                count += 1
            if (colIndex > 0):
               count += 1
            if (colIndex + groupSize < self.nrCols):
                count += 1
        
        # unavailable seats - one row underneath
        if (rowIndex + 1 < self.nrRows):
            for i in range(groupSize):
                count += 1
            if (colIndex > 0):
                count += 1
            if (colIndex + groupSize < self.nrCols):
                count += 1

        # unavailable seats - left and right sides (2 seats each)
        if (colIndex > 0):
            count += 1
        if (colIndex > 1):
            count += 1
        if (colIndex + groupSize < self.nrCols):
            count += 1
        if (colIndex + groupSize + 1 < self.nrCols):
            count += 1

        return count
    
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
        
        self.totalPlaced += groupSize

    def findSeating(self, groupSize) -> [(int, int)]:
        """
        iteratively check each row until a row is found where this group fits
        places the group on that row as far to the left as possible
        returns true if a the group is placed, false otherwise
        """
        seats = []
        # check if group is smaller or equal to number of columns
        if (groupSize > self.nrCols):
            return []
        
        # check for each row if group fits
        for y in range(nrRows):
            availableSeats = [x for x in self.getAvailableSeats(y) if x[1] >= groupSize]
            if (len(availableSeats) > 0):
                # a possible seating is found, take the first seating and place group there
                for availableSeat in availableSeats:
                    # seating: (int, int) = availableSeat
                    seats.append((y, availableSeat[0]))
                    # self.placeGroup(y, seating[0], groupSize)
                    # self.totalPlaced += groupSize
                    # self.totalRemainingPlaces -= groupSize
                # return True

        return seats



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
    
    while not queue.empty():
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
                    if (cinemaCopy.findSeating(groupIndex + 1)):
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
    cinema.createEdges()
    solution = approximation.independent_set.maximum_independent_set(cinema.graph)
    for group in solution:
        cinema.placeGroup(group[1][0], group[1][1], group[0] + 1)
        # print(cinema.layout)
    
    cinema.printCinema()

    # bestSolution = solve(cinema, nrGroupsTotal)

    # bestSolution.printCinema()

    totalVisitors: int = 0
    for i in range(len(nrGroupsTotal)):
        totalVisitors += nrGroupsTotal[i] * (i + 1)
        
    
    print(f'placed: {cinema.totalPlaced} out of {totalVisitors}')