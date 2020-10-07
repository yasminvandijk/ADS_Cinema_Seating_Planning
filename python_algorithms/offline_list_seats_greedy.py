# Implements implementation of a list of seats with greedy placement


import numpy as np
import time
import sys

class Cinema(object):
    def __init__(self, nrRows: int, nrCols: int, layout):
        self.nrRows = nrRows
        self.nrCols = nrCols
        self.layout = layout
        self.seatList = []  # 1: [(1, 1), (2, 2), ...]
        self.initSeatList()

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
    
    def initSeatList(self):
        for row in range(self.nrRows):
            self.seatList.append(dict())
            self.updateRowSeatList(row)
    
    def updateRowSeatList(self, rowIndex: int):
        availableSeats = self.getAvailableSeats(rowIndex)
        self.seatList[rowIndex] = dict()

        for seat in availableSeats:
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
    
    def markUnavailable(self, rowIndex: int, colIndex: int):
        """
        sets an empty, available seat ('1') to an unavailable seat ('+')
        doesn't check indexes for array bounds
        """
        if (self.layout[rowIndex, colIndex] == '1'):
            self.layout[rowIndex, colIndex] = '+'
    
    def placeGroup(self, rowIndex: int, colIndex: int, groupSize: int):
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
        
        for rowIndex in range(self.nrRows):
            if groupSize in self.seatList[rowIndex]:
                if len(self.seatList[rowIndex][groupSize]) != 0:
                    # print(f'exact number of {groupSize} seats found')
                    
                    # print(self.seatList[rowIndex][groupSize])
                    colIndex: int = self.seatList[rowIndex][groupSize][0]
                    self.placeGroup(rowIndex, colIndex, groupSize)
                    
                    self.updateRowsSeatList(rowIndex)

                    # self.printCinema()
                    return True
        
        # check for each row if group fits
        for y in range(nrRows):
            availableSeats = [x for x in self.getAvailableSeats(y) if x[1] >= groupSize]
            if (len(availableSeats) > 0):
                # a possible seating is found, take the first seating and place group there
                seating: (int, int) = availableSeats[0]
                self.placeGroup(y, seating[0], groupSize)

                self.updateRowsSeatList(y)
                #self.printCinema()
                return True

        return False

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

    start = time.time()
    # loop over groups in descending group size
    for index in reversed(range(len(nrGroupsTotal))):
        for _ in range(nrGroupsTotal[index]):
            current = time.time()
            if current - start > 1800:  # set 30min timeout limit
                print(-1)
                print(-1)
                sys.exit()

            if (cinema.findSeating(index + 1)):
                nrGroupsPlaced[index] = nrGroupsPlaced[index] + 1
            else:
                break

    # output
    # cinema.printOutput()
    
    # print some extra info
    # cinema.printCinema()
    # print(f'groups: {nrGroupsTotal}')
    # print(f'placed: {nrGroupsPlaced}')

    totalVisitors: int = 0
    totalPlaced: int = 0
    
    for i in range(len(nrGroupsTotal)):
        totalVisitors = totalVisitors + nrGroupsTotal[i] * (i + 1)
        totalPlaced = totalPlaced + nrGroupsPlaced[i] * (i + 1)
    
    # print(f'placed: {totalPlaced} out of {totalVisitors}')
    print(totalPlaced)
    print(np.count_nonzero(cinema.layout == '+'))
