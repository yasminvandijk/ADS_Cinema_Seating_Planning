import numpy as np

class Cinema(object):
    def __init__(self, nrRows: int, nrCols: int, layout):
        self.nrRows = nrRows
        self.nrCols = nrCols
        self.layout = layout

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
    
    def findSeating(self, groupSize: int) -> (int, int):
        """
        iteratively check each row until a row is found where this group fits
        places the group on that row as far to the left as possible
        returns (rowIndex + 1, colIndex + 1) if a the group is placed, (0, 0) otherwise
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
                #self.printCinema()
                return (y + 1, seating[0] + 1)

        return (0, 0)

if __name__ == '__main__':
    # number of rows and columns
    nrRows = int(input())
    nrCols = int(input())

    # cinema layout
    layout = np.empty((nrRows, nrCols), dtype = str)
    for i in range(nrRows):
        layout[i] = [b for b in input()]

    # read in group sizes
    groupSizes = np.array([int(nr) for nr in input().split()])

    # number of groups in total for each group size
    nrGroupsTotal = np.full((8), 0, dtype=int)
    # number of groups placed for each group size
    nrGroupsPlaced = np.full((8), 0, dtype=int)

    cinema = Cinema(nrRows, nrCols, layout)

    # try to place groups one by one
    for groupSize in groupSizes:
        if groupSize == 0:
            break
        (y, x) = cinema.findSeating(groupSize)
        nrGroupsTotal[groupSize - 1] = nrGroupsTotal[groupSize - 1] + 1
        if ((y, x) != (0, 0)):
            nrGroupsPlaced[groupSize - 1] = nrGroupsPlaced[groupSize - 1] + 1
        print(f'{y} {x}')
    
    # print some extra info
    cinema.printCinema()
    print(f'groups: {nrGroupsTotal}')
    print(f'placed: {nrGroupsPlaced}')

    totalVisitors: int = 0
    totalPlaced: int = 0

    for i in range(len(nrGroupsTotal)):
        totalVisitors = totalVisitors + nrGroupsTotal[i] * (i + 1)
        totalPlaced = totalPlaced + nrGroupsPlaced[i] * (i + 1)
    
    print(f'placed: {totalPlaced} out of {totalVisitors}')
