# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 21:17:18 2022

@author: Lenovo
"""

from utils import *

def solveCase(requirement, stock):
    solver = newSolver('Cutting Stock', True)
    
    # VARIABLES
    # length of arrays
    R = len(requirement)    # i = 1, 2, 3, ..., R (requirement)
    S = len(stock)          # j = 1, 2, 3, ..., S (stock)
    
    # x[i][j]: req i is cutted from stock j
    x = [[solver.IntVar(0, 1, f'x_{i}_{j}') for j in range(S)] for i in range(R)]
    
    # y[j]: stock s is used
    y = [solver.IntVar(0,1, f'y_{j}') for j in range(S)]
    
    # RESTRICTIONS
    # Demand fullfilment
    for i in range(R):
        solver.Add(sum(x[i][j] for j in range(S)) == 1)
    
    # Stock use limit
    for j in range(S):
        solver.Add(sum(requirement[i] * x[i][j] for i in range(R)) <= y[j] * stock[j])
    
    # Stock used to deliver demand 
    for i in range(R):
        for j in range(S):
            solver.Add(x[i][j] <= y[j])
            
    # OBJECTIVE
    # # Number of stock items used
    # Cost = sum(y[j] for j in range(S)) 
    
    # Waste
    Cost = sum(y[j]*stock[j] - \
                sum(x[i][j]*requirement[i] for i in range(R)) \
                    for j in range(S))
    solver.Minimize(Cost)
    
    # MODEL SOLUTION
    status = solver.Solve()
        # 0: optimal
        # 1: feasible
        # 2: infeasible
        # 3: unbounded
        # 4: abnormal
        # 6: notsolved
        # 7: not stock
        # 8: error in file
    if status == 0:
        xSol = [[x[i][j].SolutionValue() for j in range(S)] for i in range(R)]
        ySol = [y[j].SolutionValue() for j in range(S)]
        Sol = [[stock[j], \
                [requirement[i] for i in range(R) if xSol[i][j] > 0]\
                    ] for j in range(S) if ySol[j] > 0]
        waste = sum(ySol[j]*stock[j] - \
                    sum(xSol[i][j]*requirement[i] for i in range(R)) \
                        for j in range(S))
        return status, Sol, waste
    else:
        return status, [], 100
    
    if status <= 1: # status: 0, 1
        xSol = [[x[i][j].SolutionValue() for j in range(S)] for i in range(R)]
        ySol = [y[j].SolutionValue() for j in range(S)]
        Sol = [ [ stock[j],[requirement[i] for i in range(R) if xSol[i][j] > 0] ] for j in range(S) if ySol[j] > 0]
        return status, ObjVal(solver), xSol, ySol, Sol
    else:
        return status, "inf", [[0 for j in range(S)] for i in range(R)], \
                [0 for j in range(S)]
# # Test
# requirement = [2, 3, 4, 2, 2, 3, 2.1, 30, 1]
# stock = [6, 10, 8, 4, 31]

# #status, sol, xSol, ySol, Sol = solveCase(requirement, stock)
# status,  Sol, waste = solveCase(requirement, stock)