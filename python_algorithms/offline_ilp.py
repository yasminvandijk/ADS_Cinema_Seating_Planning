import gurobipy as gp
from gurobipy import GRB
import numpy as np

NLAYERS = 8

def createModel(nrRows, nrCols, layout, nrGroupsTotal):

    try:
        # Create a new model
        model = gp.Model('cinema')

        x = model.addVars(NLAYERS, nrRows, nrCols, vtype = GRB.BINARY, name = 'x')  # x[i, r, c]
        seats = model.addVars(nrRows, nrCols, vtype = GRB.BINARY, name = 'seats')   # X[i]

        for row in range(nrRows):
            for col in range(nrCols):
                model.addConstrs(((seats[row, col] == 0) >> (x[layer, row, col] == 0)) for layer in range(NLAYERS)) # cannot seat people where there is no seat
                if layout[row, col] == '1':
                    model.addConstr(seats[row, col] == 1)
                else:
                    model.addConstr(seats[row, col] == 0)

        model.addConstrs(x.sum('*', i, j) <= 1 for i in range(nrRows) for j in range(nrCols))   # the sum of people seating on the same spot on all layers has to be at most 1
        # model.addConstrs((x[i, r, c] == 1) >> (x[j, r, c] == 0) for i in range(NLAYERS) for j in range(NLAYERS) for r in range(nrRows) for c in range(nrCols) if i != j)
        model.setObjective(gp.quicksum(x), GRB.MAXIMIZE)   # maximise the total number of people

        for i in range(NLAYERS - 1):
            for j in range(i, NLAYERS):
                for r in range(nrRows):
                    for c in range(nrCols):
                        # model.addConstr((x[i, r, c] == 1) >> (x[j, r, c] == 0))
                        # model.addConstr((x[j, r, c] == 1) >> (x[i, r, c] == 0))
                        for k in range(-2, 3):  # same row
                            try:
                                model.addConstr((x[i, r, c] == 1) >> (x[j, r, c + k + i] == 0))
                                model.addConstr((x[j, r, c] == 1) >> (x[i, r, c + k + j] == 0))

                                # model.addConstr(x[i, r, c] * x[j, r, c + k + i] == 0)
                                # model.addConstr(x[j, r, c] * x[i, r, c + k + j] == 0)

                                # pass
                            except KeyError:
                                pass
                        for k in range(-1, 2):  # one row apart
                            for l in range(-1, 2):  # check for columns
                                try:
                                    model.addConstr((x[i, r, c] == 1) >> (x[j, r + k, c + l + i] == 0))
                                    model.addConstr((x[j, r, c] == 1) >> (x[i, r + k, c + l + j] == 0))

                                    # model.addConstr(x[i, r, c] * x[j, r + k, c + l + i] == 0)
                                    # model.addConstr(x[j, r, c] * x[i, r + k, c + l + j] == 0)

                                    # pass
                                except KeyError:
                                    pass
        
        for i in range(NLAYERS):
            model.addConstr(x.sum(i, '*', '*') <= (i + 1) * nrGroupsTotal[i])
        
        model.optimize()

        # print(model.objValue)

        return model.getAttr('x', x)

        # Create variables
        # x = m.addVar(vtype=GRB.BINARY, name="x")
        # y = m.addVar(vtype=GRB.BINARY, name="y")
        # z = m.addVar(vtype=GRB.BINARY, name="z")

        # # Set objective
        # m.setObjective(x + y + 2 * z, GRB.MAXIMIZE)

        # # Add constraint: x + 2 y + 3 z <= 4
        # m.addConstr(x + 2 * y + 3 * z <= 4, "c0")

        # # Add constraint: x + y >= 1
        # m.addConstr(x + y >= 1, "c1")

        # # Optimize model
        # m.optimize()

        # for v in m.getVars():
        #     print('%s %g' % (v.varName, v.x))

        # print('Obj: %g' % m.objVal)

    except gp.GurobiError as e:
        print('Error code ' + str(e.errno) + ': ' + str(e))

    except AttributeError:
        print('Encountered an attribute error')

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
        
        # check for each row if group fits
        for y in range(nrRows):
            availableSeats = [x for x in self.getAvailableSeats(y) if x[1] >= groupSize]
            if (len(availableSeats) > 0):
                # a possible seating is found, take the first seating and place group there
                seating: (int, int) = availableSeats[0]
                self.placeGroup(y, seating[0], groupSize)
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

    cinemas = []
    for i in range(NLAYERS):
        cinemas.append(Cinema(nrRows, nrCols, layout))

    solution = createModel(nrRows, nrCols, layout, nrGroupsTotal)
    for seat in solution:
        if solution[seat] == 1:
            cinemas[seat[0]].placeGroup(seat[1], seat[2], 1)
    # loop over groups in descending group size
    # for index in reversed(range(len(nrGroupsTotal))):
    #     for _ in range(nrGroupsTotal[index]):
    #         if (cinema.findSeating(index + 1)):
    #             nrGroupsPlaced[index] = nrGroupsPlaced[index] + 1
    #         else:
    #             break

    # output
    for cinema in cinemas:
        cinema.printOutput()
    
    # print some extra info
    # cinema.printCinema()
    # print(f'groups: {nrGroupsTotal}')
    # print(f'placed: {nrGroupsPlaced}')

    # totalVisitors: int = 0
    # totalPlaced: int = 0
    
    # for i in range(len(nrGroupsTotal)):
    #     totalVisitors = totalVisitors + nrGroupsTotal[i] * (i + 1)
    #     totalPlaced = totalPlaced + nrGroupsPlaced[i] * (i + 1)
    
    # print(f'placed: {totalPlaced} out of {totalVisitors}')
