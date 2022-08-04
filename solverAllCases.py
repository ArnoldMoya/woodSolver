# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 10:43:34 2022

@author: Lenovo
"""
from solverCase import *

def solverAllCases(requirement, stock):
    strategy = {}
    for material in requirement.keys():
        try:
            status,  Sol, waste = solveCase(requirement[material], stock[material])
        except:
            # infeasible because there is no stock. New status: 7
            status,  Sol, waste = 7, [], 100
        #status,  Sol, waste = solveCase(requirement[material], stock[material])
        #print(material, "status:",  status," - Sol:", Sol, " - waste:", waste)
        strategy[material] = [status, Sol]
    return strategy

# # Test
# stock = {"tipo1": [2, 2, 4], "tipo2": [4, 3,2, 5], "tipo3": [2, 4]}
# requirement = {"tipo1": [2, 2, 4], "tipo2": [3,2.1], "tipo3": [10], "tipo4": [1, 2]}

# strategy = solverAllCases(requirement, stock)
