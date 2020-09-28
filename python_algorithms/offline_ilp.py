import gurobipy as gp
from gurobipy import GRB

N = 12
M = 12
NLAYERS = 8
X = [4, 8, 2, 1, 2, 4, 0, 0]
try:
    # Create a new model
    model = gp.Model('cinema')

    x = model.addVar((NLAYERS, N, M),vtype = GRB.BINARY, name = 'x')  # x[i, r, c]
    # X = model.addVar((NLAYERS), vtype = GRB.BINARY, name = 'X')   # X[i]

    model.setObjective(x.sum(), GRB.MAXIMIZE)   # maximise the total number of people

    for i in range(NLAYERS - 1):
        for j in range(i + 1, NLAYERS):
            for r in range(N):
                for c in range(M):
                    for k in range(-2, 3):
                        model.addConstr(x[i, r, c] * x[j, r, c + k] == 0)
                    for k in range(-1, 2):
                        for l in range(-1, 2):
                            model.addConstr(x[i, r, c] * x[j, r + k, c + l] == 0)
    
    for i in range(NLAYERS):
        model.addConstr(x[i].sum() <= (i + 1) * X[i])
    
    model.optimize()

    print(model.objValue)


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